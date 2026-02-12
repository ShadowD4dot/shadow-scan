#!/usr/bin/env python3
"""
Direct Scan - Escaneo directo sin enumeración de subdominios
Útil cuando el dominio no tiene subdominios públicos o quieres escanear rápido
"""

import subprocess
import json
import sys
from pathlib import Path
from datetime import datetime
import argparse

def run_direct_scan(target: str, severity: str = "critical,high,medium"):
    """Escanear directamente un dominio sin subfinder"""
    
    print(f"\n{'='*60}")
    print(f"🎯 ESCANEO DIRECTO - {target}")
    print(f"{'='*60}\n")
    
    # Crear directorio de salida
    output_dir = Path("direct_scans")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    scan_dir = output_dir / f"{target.replace(':', '_').replace('/', '_')}_{timestamp}"
    scan_dir.mkdir(exist_ok=True)
    
    # Asegurar protocolo
    if not target.startswith(('http://', 'https://')):
        urls = [f'https://{target}', f'http://{target}']
    else:
        urls = [target]
    
    print(f"🌐 [1/2] Verificando accesibilidad con httpx...")
    
    # Crear archivo temporal con URLs
    urls_file = scan_dir / "urls.txt"
    with open(urls_file, 'w') as f:
        f.write('\n'.join(urls))
    
    # Ejecutar httpx
    httpx_output = scan_dir / "httpx_result.json"
    
    try:
        cmd = [
            'httpx',
            '-l', str(urls_file),
            '-title',
            '-tech-detect',
            '-status-code',
            '-content-length',
            '-json',
            '-o', str(httpx_output),
            '-silent',
            '-timeout', '10'
        ]
        
        subprocess.run(cmd, check=True, timeout=60)
        
        # Leer resultados
        alive_hosts = []
        if httpx_output.exists():
            with open(httpx_output) as f:
                for line in f:
                    if line.strip():
                        try:
                            alive_hosts.append(json.loads(line))
                        except:
                            pass
        
        if not alive_hosts:
            print(f"   ❌ El dominio no responde o no es accesible")
            print(f"   Verifica:")
            print(f"   1. Que el dominio existe y es accesible")
            print(f"   2. No estás detrás de un firewall/proxy")
            print(f"   3. El dominio no requiere autenticación")
            return
        
        print(f"   ✅ Dominio accesible: {alive_hosts[0]['url']}")
        
        # Mostrar info
        host = alive_hosts[0]
        print(f"   📊 Status: {host.get('status_code', 'N/A')}")
        print(f"   📄 Title: {host.get('title', 'N/A')}")
        techs = host.get('technologies', [])
        if techs:
            print(f"   🔧 Tecnologías: {', '.join(techs[:5])}")
        
    except Exception as e:
        print(f"   ❌ Error en httpx: {e}")
        return
    
    # Escanear con Nuclei
    print(f"\n🎯 [2/2] Escaneando vulnerabilidades (severity: {severity})...")
    
    nuclei_output = scan_dir / "vulnerabilities.json"
    target_url = alive_hosts[0]['url']
    
    try:
        cmd = [
            'nuclei',
            '-u', target_url,
            '-severity', severity,
            '-json',
            '-o', str(nuclei_output),
            '-silent',
            '-c', '50',
            '-timeout', '10'
        ]
        
        subprocess.run(cmd, check=True, timeout=1800)
        
        # Leer vulnerabilidades
        vulnerabilities = []
        if nuclei_output.exists():
            with open(nuclei_output) as f:
                for line in f:
                    if line.strip():
                        try:
                            vulnerabilities.append(json.loads(line))
                        except:
                            pass
        
        # Estadísticas
        from collections import defaultdict
        severity_counts = defaultdict(int)
        
        for vuln in vulnerabilities:
            sev = vuln.get('info', {}).get('severity', 'unknown')
            severity_counts[sev] += 1
        
        print(f"   ✅ {len(vulnerabilities)} vulnerabilidades detectadas")
        
        if vulnerabilities:
            for sev in ['critical', 'high', 'medium', 'low']:
                if sev in severity_counts:
                    count = severity_counts[sev]
                    emoji = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}.get(sev, '⚪')
                    print(f"      {emoji} {sev.upper()}: {count}")
        
    except subprocess.TimeoutExpired:
        print("   ⚠️  Nuclei timeout - usando resultados parciales")
        vulnerabilities = []
    except Exception as e:
        print(f"   ❌ Error en nuclei: {e}")
        vulnerabilities = []
    
    # Crear reporte
    report = {
        'scan_info': {
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'scan_type': 'direct',
            'scan_directory': str(scan_dir)
        },
        'host_info': alive_hosts[0] if alive_hosts else {},
        'vulnerabilities': vulnerabilities,
        'statistics': {
            'total_vulnerabilities': len(vulnerabilities),
            'vulnerability_severity': dict(severity_counts)
        }
    }
    
    report_file = scan_dir / "report.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    # Resumen
    print(f"\n{'='*60}")
    print(f"📊 RESUMEN")
    print(f"{'='*60}")
    print(f"🎯 Target: {target}")
    print(f"✅ Accesible: {'Sí' if alive_hosts else 'No'}")
    print(f"🔥 Vulnerabilidades: {len(vulnerabilities)}")
    
    if severity_counts:
        print(f"\n📈 Por severidad:")
        for sev in ['critical', 'high', 'medium', 'low']:
            if sev in severity_counts:
                emoji = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}.get(sev, '⚪')
                print(f"   {emoji} {sev.upper()}: {severity_counts[sev]}")
    
    print(f"\n💾 Reporte guardado en: {report_file}")
    print(f"{'='*60}\n")
    
    return report_file

def main():
    parser = argparse.ArgumentParser(
        description='Direct Scan - Escaneo directo sin enumeración de subdominios',
        epilog="""
Ejemplos:
  python3 direct_scan.py -u egdp-dev.avangenio.net
  python3 direct_scan.py -u https://example.com -s critical,high
  python3 direct_scan.py -u api.example.com -s critical,high,medium,low
        """
    )
    
    parser.add_argument('-u', '--url', required=True,
                       help='URL o dominio a escanear directamente')
    parser.add_argument('-s', '--severity',
                       default='critical,high,medium',
                       help='Severidades de Nuclei (default: critical,high,medium)')
    
    args = parser.parse_args()
    
    try:
        run_direct_scan(args.url, args.severity)
        print("✅ Escaneo directo completado")
    except KeyboardInterrupt:
        print("\n\n⚠️  Escaneo interrumpido")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
