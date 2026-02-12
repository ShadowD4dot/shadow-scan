#!/usr/bin/env python3
"""
Shadow-Scan - Automated Attack Surface Scanner
Combina subfinder, httpx y nuclei para reconocimiento automatizado
"""

import subprocess
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import argparse
from dataclasses import dataclass, asdict
import sqlite3
from collections import defaultdict
from urllib.parse import urlparse
import re

@dataclass
class ScanResult:
    """Estructura para almacenar resultados del escaneo"""
    domain: str
    timestamp: str
    subdomains: List[str]
    alive_hosts: List[Dict]
    vulnerabilities: List[Dict]
    stats: Dict

def extract_domain(target: str) -> str:
    """
    Extraer dominio limpio de una URL o string
    
    Ejemplos:
        https://example.com -> example.com
        http://sub.example.com/path -> sub.example.com
        example.com -> example.com
    """
    # Si contiene protocolo, parsear como URL
    if '://' in target:
        parsed = urlparse(target)
        domain = parsed.netloc or parsed.path
    else:
        # Remover http/https si está presente sin ://
        domain = target.replace('http:', '').replace('https:', '')
        # Remover barras
        domain = domain.strip('/')
    
    # Limpiar cualquier path restante
    domain = domain.split('/')[0]
    
    # Limpiar puerto si existe
    domain = domain.split(':')[0]
    
    return domain.strip()

def sanitize_dirname(name: str) -> str:
    """
    Sanitizar nombre para crear directorios válidos
    Reemplaza caracteres inválidos por guiones bajos
    """
    # Remover caracteres inválidos para nombres de archivos/directorios
    invalid_chars = r'[<>:"/\\|?*\s]'
    sanitized = re.sub(invalid_chars, '_', name)
    
    # Remover puntos al inicio o final
    sanitized = sanitized.strip('._')
    
    return sanitized

class ShadowScanner:
    """Motor principal del escáner"""
    
    def __init__(self, target: str, output_dir: str = "scan_results"):
        # Extraer y limpiar el dominio
        self.original_target = target
        self.target = extract_domain(target)
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Directorio específico para este escaneo (con nombre sanitizado)
        safe_dirname = sanitize_dirname(self.target)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.scan_dir = self.output_dir / f"{safe_dirname}_{timestamp}"
        self.scan_dir.mkdir(exist_ok=True)
        
        self.results = {
            'subdomains': [],
            'alive_hosts': [],
            'vulnerabilities': []
        }
        
    def check_tools(self) -> bool:
        """Verificar que las herramientas necesarias están instaladas"""
        tools = ['subfinder', 'httpx', 'nuclei']
        missing = []
        
        for tool in tools:
            try:
                subprocess.run([tool, '-version'], 
                             capture_output=True, 
                             check=True,
                             timeout=5)
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                missing.append(tool)
        
        if missing:
            print(f"❌ Herramientas faltantes: {', '.join(missing)}")
            print("\n📥 Instalación:")
            print("go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest")
            print("go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest")
            print("go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest")
            return False
        
        return True
    
    def run_subfinder(self) -> List[str]:
        """Ejecutar subfinder para encontrar subdominios"""
        print(f"\n🔍 [1/3] Enumerando subdominios para {self.target}...")
        
        output_file = self.scan_dir / "subdomains.txt"
        
        try:
            cmd = [
                'subfinder',
                '-d', self.target,
                '-all',
                '-recursive',
                '-o', str(output_file),
                '-silent'
            ]
            
            subprocess.run(cmd, check=True, timeout=300)
            
            # Leer resultados
            subdomains = []
            if output_file.exists():
                with open(output_file) as f:
                    subdomains = [line.strip() for line in f if line.strip()]
            
            # Si no se encontraron subdominios, incluir el dominio principal
            if not subdomains:
                print(f"   ⚠️  No se encontraron subdominios públicos")
                print(f"   💡 Incluyendo dominio principal: {self.target}")
                subdomains = [self.target]
                
                # Guardar en archivo
                with open(output_file, 'w') as f:
                    f.write(self.target + '\n')
            
            self.results['subdomains'] = subdomains
            print(f"   ✅ Total de targets: {len(subdomains)}")
            if len(subdomains) > 1:
                print(f"      → {len(subdomains) - 1} subdominios + 1 dominio principal")
            
            return subdomains
            
        except subprocess.TimeoutExpired:
            print("   ⚠️  Subfinder timeout - usando dominio principal")
            subdomains = [self.target]
            with open(output_file, 'w') as f:
                f.write(self.target + '\n')
            return subdomains
        except Exception as e:
            print(f"   ❌ Error en subfinder: {e}")
            print(f"   💡 Continuando con dominio principal: {self.target}")
            subdomains = [self.target]
            with open(output_file, 'w') as f:
                f.write(self.target + '\n')
            return subdomains
    
    def run_httpx(self, targets: List[str]) -> List[Dict]:
        """Ejecutar httpx para verificar hosts activos"""
        print(f"\n🌐 [2/3] Verificando hosts activos ({len(targets)} targets)...")
        
        if not targets:
            print("   ⚠️  No hay targets para verificar")
            return []
        
        # Crear archivo temporal con targets
        targets_file = self.scan_dir / "targets.txt"
        with open(targets_file, 'w') as f:
            f.write('\n'.join(targets))
        
        output_file = self.scan_dir / "alive_hosts.json"
        
        try:
            cmd = [
                'httpx',
                '-l', str(targets_file),
                '-title',
                '-tech-detect',
                '-status-code',
                '-content-length',
                '-json',
                '-o', str(output_file),
                '-silent',
                '-threads', '50',
                '-timeout', '10'
            ]
            
            subprocess.run(cmd, check=True, timeout=600)
            
            # Leer resultados JSON
            if output_file.exists():
                alive_hosts = []
                with open(output_file) as f:
                    for line in f:
                        if line.strip():
                            try:
                                alive_hosts.append(json.loads(line))
                            except json.JSONDecodeError:
                                continue
                
                self.results['alive_hosts'] = alive_hosts
                print(f"   ✅ {len(alive_hosts)} hosts activos detectados")
                return alive_hosts
                
        except subprocess.TimeoutExpired:
            print("   ⚠️  httpx timeout - usando resultados parciales")
        except Exception as e:
            print(f"   ❌ Error en httpx: {e}")
        
        return []
    
    def run_nuclei(self, targets: List[str], severity: str = "critical,high,medium") -> List[Dict]:
        """Ejecutar nuclei para detectar vulnerabilidades con reintentos automáticos"""
        print(f"\n🎯 [3/3] Escaneando vulnerabilidades (severity: {severity})...")
        
        if not targets:
            print("   ⚠️  No hay targets para escanear")
            return []
        
        # Extraer URLs de los hosts activos
        urls = []
        for host in targets:
            if isinstance(host, dict):
                urls.append(host.get('url', ''))
            else:
                urls.append(host)
        
        urls = [u for u in urls if u]
        
        if not urls:
            print("   ⚠️  No hay URLs válidas")
            return []
        
        targets_file = self.scan_dir / "nuclei_targets.txt"
        with open(targets_file, 'w') as f:
            f.write('\n'.join(urls))
        
        output_file = self.scan_dir / "vulnerabilities.json"
        
        # Reintentos automáticos para errores de conexión
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                cmd = [
                    'nuclei',
                    '-l', str(targets_file),
                    '-severity', severity,
                    '-jsonl',
                    '-o', str(output_file),
                    '-silent',
                    '-c', '20',
                    '-timeout', '15',
                    '-retries', '2',
                    '-max-host-error', '20',
                    '-rate-limit', '100'
                ]
                
                subprocess.run(cmd, check=True, timeout=1800)
                
                # Leer resultados
                vulnerabilities = []
                if output_file.exists():
                    with open(output_file) as f:
                        for line in f:
                            if line.strip():
                                try:
                                    vulnerabilities.append(json.loads(line))
                                except json.JSONDecodeError:
                                    continue
                
                self.results['vulnerabilities'] = vulnerabilities
                
                # Estadísticas por severidad
                severity_counts = defaultdict(int)
                for vuln in vulnerabilities:
                    sev = vuln.get('info', {}).get('severity', 'unknown')
                    severity_counts[sev] += 1
                
                print(f"   ✅ {len(vulnerabilities)} vulnerabilidades detectadas")
                for sev, count in sorted(severity_counts.items()):
                    emoji = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}.get(sev, '⚪')
                    print(f"      {emoji} {sev.upper()}: {count}")
                
                return vulnerabilities
                
            except subprocess.TimeoutExpired:
                print("   ⚠️  Nuclei timeout - usando resultados parciales")
                break
            except Exception as e:
                error_msg = str(e).lower()
                # Reintentar solo para errores de conexión
                if any(keyword in error_msg for keyword in ['unreachable', 'refused', 'timeout', 'connection']):
                    retry_count += 1
                    if retry_count < max_retries:
                        print(f"   🔄 Error de conexión detectado. Reintentando ({retry_count}/{max_retries-1})...")
                        import time
                        time.sleep(5 * retry_count)  # Incrementar delay con cada reintento
                        continue
                    else:
                        print(f"   ❌ Error persistente en nuclei después de {max_retries} intentos: {e}")
                else:
                    print(f"   ❌ Error en nuclei: {e}")
                break
        
        return []
    
    def generate_stats(self) -> Dict:
        """Generar estadísticas del escaneo"""
        stats = {
            'total_subdomains': len(self.results['subdomains']),
            'total_alive_hosts': len(self.results['alive_hosts']),
            'total_vulnerabilities': len(self.results['vulnerabilities']),
            'scan_time': datetime.now().isoformat(),
            'target': self.target
        }
        
        # Severidad de vulnerabilidades
        severity_breakdown = defaultdict(int)
        for vuln in self.results['vulnerabilities']:
            sev = vuln.get('info', {}).get('severity', 'unknown')
            severity_breakdown[sev] += 1
        
        stats['vulnerability_severity'] = dict(severity_breakdown)
        
        # Tecnologías detectadas
        technologies = set()
        for host in self.results['alive_hosts']:
            techs = host.get('technologies', [])
            if isinstance(techs, list):
                technologies.update(techs)
        
        stats['technologies_found'] = list(technologies)
        
        return stats
    
    def save_results(self) -> str:
        """Guardar todos los resultados en un archivo JSON consolidado"""
        stats = self.generate_stats()
        
        final_report = {
            'scan_info': {
                'target': self.target,
                'timestamp': datetime.now().isoformat(),
                'scan_directory': str(self.scan_dir)
            },
            'statistics': stats,
            'subdomains': self.results['subdomains'],
            'alive_hosts': self.results['alive_hosts'],
            'vulnerabilities': self.results['vulnerabilities']
        }
        
        report_file = self.scan_dir / "full_report.json"
        with open(report_file, 'w') as f:
            json.dump(final_report, f, indent=2)
        
        print(f"\n💾 Reporte completo guardado en: {report_file}")
        return str(report_file)
    
    def run_full_scan(self, nuclei_severity: str = "critical,high,medium") -> Dict:
        """Ejecutar el pipeline completo de escaneo"""
        print(f"\n{'='*60}")
        print(f"🕵️  SHADOW-SCAN - Análisis de Superficie de Ataque")
        print(f"{'='*60}")
        print(f"🎯 Target: {self.target}")
        print(f"📁 Output: {self.scan_dir}")
        print(f"{'='*60}")
        
        # 1. Enumerar subdominios
        subdomains = self.run_subfinder()
        
        # 2. Verificar hosts activos
        alive_hosts = self.run_httpx(subdomains)
        
        # 3. Escanear vulnerabilidades
        vulnerabilities = self.run_nuclei(alive_hosts, nuclei_severity)
        
        # 4. Guardar resultados
        report_path = self.save_results()
        
        # 5. Mostrar resumen
        self.print_summary()
        
        return {
            'report_path': report_path,
            'stats': self.generate_stats(),
            'results': self.results
        }
    
    def print_summary(self):
        """Imprimir resumen ejecutivo del escaneo"""
        stats = self.generate_stats()
        
        print(f"\n{'='*60}")
        print("📊 RESUMEN EJECUTIVO")
        print(f"{'='*60}")
        print(f"🌐 Subdominios descubiertos: {stats['total_subdomains']}")
        print(f"✅ Hosts activos: {stats['total_alive_hosts']}")
        print(f"🎯 Vulnerabilidades totales: {stats['total_vulnerabilities']}")
        
        if stats['vulnerability_severity']:
            print(f"\n🔥 Desglose por severidad:")
            severity_order = ['critical', 'high', 'medium', 'low', 'info']
            for sev in severity_order:
                if sev in stats['vulnerability_severity']:
                    count = stats['vulnerability_severity'][sev]
                    emoji = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢', 'info': '⚪'}.get(sev, '⚪')
                    print(f"   {emoji} {sev.upper()}: {count}")
        
        if stats['technologies_found']:
            print(f"\n🔧 Tecnologías detectadas ({len(stats['technologies_found'])}):")
            for tech in sorted(stats['technologies_found'])[:10]:
                print(f"   • {tech}")
            if len(stats['technologies_found']) > 10:
                print(f"   ... y {len(stats['technologies_found']) - 10} más")
        
        print(f"\n{'='*60}")


def main():
    parser = argparse.ArgumentParser(
        description='Shadow-Scan - Automated Attack Surface Scanner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  %(prog)s -d example.com
  %(prog)s -d example.com -s critical,high
  %(prog)s -d example.com -o my_scans
        """
    )
    
    parser.add_argument('-d', '--domain', required=True,
                       help='Dominio objetivo para escanear')
    parser.add_argument('-s', '--severity', 
                       default='critical,high,medium',
                       help='Severidades de Nuclei (default: critical,high,medium)')
    parser.add_argument('-o', '--output', 
                       default='scan_results',
                       help='Directorio de salida (default: scan_results)')
    
    args = parser.parse_args()
    
    # Crear escáner
    scanner = ShadowScanner(args.domain, args.output)
    
    # Verificar herramientas
    if not scanner.check_tools():
        sys.exit(1)
    
    # Ejecutar escaneo completo
    try:
        results = scanner.run_full_scan(args.severity)
        print(f"\n✅ Escaneo completado exitosamente")
        print(f"📄 Reporte: {results['report_path']}")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Escaneo interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error durante el escaneo: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()