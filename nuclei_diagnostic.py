#!/usr/bin/env python3
"""
Diagnóstico Avanzado de Nuclei para Shadow-Scan
Verifica conectividad, configuración y ofrece soluciones
"""

import subprocess
import json
import sys
import platform
from pathlib import Path
from typing import Dict, List, Tuple
import socket
import urllib.request
import urllib.error

class NucleiDiagnostic:
    """Herramienta de diagnóstico para Nuclei"""
    
    def __init__(self):
        self.is_windows = platform.system() == "Windows"
        self.results = {
            'connectivity': {},
            'nuclei_config': {},
            'recommendations': []
        }
    
    def run_all_checks(self):
        """Ejecutar todos los diagnósticos"""
        print("🔍 SHADOW-SCAN - Diagnóstico de Nuclei")
        print("=" * 60)
        
        self.check_nuclei_installed()
        self.check_nuclei_version()
        self.check_network_connectivity()
        self.check_dns_resolution()
        self.check_firewall_ports()
        self.check_nuclei_templates()
        self.suggest_optimal_config()
        
        self.print_report()
    
    def check_nuclei_installed(self):
        """Verificar si Nuclei está instalado"""
        print("\n📦 Verificando instalación de Nuclei...")
        try:
            result = subprocess.run(
                ['nuclei', '-version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print("   ✅ Nuclei instalado correctamente")
                self.results['nuclei_config']['installed'] = True
                self.results['nuclei_config']['version_output'] = result.stdout.strip()
            else:
                print("   ❌ Error al ejecutar nuclei")
                self.results['nuclei_config']['installed'] = False
        except FileNotFoundError:
            print("   ❌ Nuclei NO instalado o no está en el PATH")
            self.results['nuclei_config']['installed'] = False
            self.results['recommendations'].append(
                "Instala Nuclei: go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest"
            )
        except Exception as e:
            print(f"   ❌ Error: {e}")
            self.results['nuclei_config']['installed'] = False
    
    def check_nuclei_version(self):
        """Obtener versión de Nuclei"""
        print("\n🔧 Información de Nuclei...")
        try:
            result = subprocess.run(
                ['nuclei', '-version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            version_info = result.stdout.strip()
            print(f"   {version_info}")
            self.results['nuclei_config']['version'] = version_info
        except Exception as e:
            print(f"   ⚠️  No se pudo obtener versión: {e}")
    
    def check_network_connectivity(self):
        """Verificar conectividad de red"""
        print("\n🌐 Verificando conectividad de red...")
        
        test_hosts = [
            ('8.8.8.8', 'Google DNS'),
            ('1.1.1.1', 'Cloudflare DNS'),
            ('google.com', 'Google.com'),
        ]
        
        for host, description in test_hosts:
            try:
                socket.gethostbyname(host)
                print(f"   ✅ {description} ({host})")
                self.results['connectivity'][description] = True
            except socket.gaierror:
                print(f"   ❌ {description} ({host}) - NO REACHABLE")
                self.results['connectivity'][description] = False
                self.results['recommendations'].append(
                    f"Revisar lo conectividad a {host} - puede haber problemas de DNS"
                )
    
    def check_dns_resolution(self):
        """Verificar resolución DNS"""
        print("\n🔎 Verificando resolución DNS...")
        
        test_domains = ['example.com', 'google.com']
        
        for domain in test_domains:
            try:
                ip = socket.gethostbyname(domain)
                print(f"   ✅ {domain} → {ip}")
            except socket.gaierror:
                print(f"   ❌ {domain} - No se puede resolver")
                self.results['recommendations'].append(
                    f"DNS no puede resolver {domain}"
                )
            except Exception as e:
                print(f"   ⚠️  Error resolviendo {domain}: {e}")
    
    def check_firewall_ports(self):
        """Verificar puertos comunes"""
        print("\n🚪 Verificando puertos comunes...")
        
        common_ports = [
            (80, 'HTTP'),
            (443, 'HTTPS'),
            (53, 'DNS'),
        ]
        
        for port, service in common_ports:
            if self.is_windows:
                try:
                    # PowerShell command en Windows
                    cmd = f"Test-NetConnection -ComputerName 8.8.8.8 -Port {port} -WarningAction SilentlyContinue"
                    result = subprocess.run(
                        ['powershell', '-Command', cmd],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    if 'True' in result.stdout:
                        print(f"   ✅ Puerto {port} ({service})")
                    else:
                        print(f"   ⚠️  Puerto {port} ({service}) - Posiblemente bloqueado")
                except Exception as e:
                    print(f"   ⚠️  No se pudo verificar puerto {port}: {e}")
            else:
                # Linux/Mac
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    result = sock.connect_ex(('8.8.8.8', port))
                    sock.close()
                    if result == 0:
                        print(f"   ✅ Puerto {port} ({service})")
                    else:
                        print(f"   ⚠️  Puerto {port} ({service}) - Posiblemente bloqueado")
                except Exception as e:
                    print(f"   ⚠️  Error verificando puerto {port}: {e}")
    
    def check_nuclei_templates(self):
        """Verificar templates de Nuclei"""
        print("\n📋 Verificando templates de Nuclei...")
        
        try:
            result = subprocess.run(
                ['nuclei', '-list'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # Contar templates
                templates = result.stdout.strip().split('\n')
                template_count = len([t for t in templates if t.strip()])
                print(f"   ✅ Templates encontrados: {template_count}")
                self.results['nuclei_config']['templates'] = template_count
            else:
                print("   ⚠️  No se pudieron listar templates")
                self.results['recommendations'].append(
                    "Ejecuta 'nuclei -update-templates' para descargar/actualizar templates"
                )
        except Exception as e:
            print(f"   ⚠️  Error listando templates: {e}")
    
    def suggest_optimal_config(self):
        """Sugerir configuración óptima"""
        print("\n⚙️  Sugerencias de Configuración...")
        
        # Análisis simple de conectividad
        connectivity_ok = sum(1 for v in self.results['connectivity'].values() if v)
        total_tests = len(self.results['connectivity'])
        
        if connectivity_ok == 0:
            print("   🔴 Problema grave de conectividad detectado")
            self.results['recommendations'].append(
                "Configuración recomendada para redes muy restrictivas: "
                "nuclei -c 5 -timeout 25 -retries 3 -max-host-error 5"
            )
        elif connectivity_ok < total_tests:
            print("   🟡 Conectividad inestable detectada")
            self.results['recommendations'].append(
                "Configuración recomendada para redes inestables: "
                "nuclei -c 10 -timeout 20 -retries 3 -max-host-error 15"
            )
        else:
            print("   🟢 Conectividad buena")
            self.results['recommendations'].append(
                "Configuración recomendada para redes estables: "
                "nuclei -c 20 -timeout 15 -retries 2 -max-host-error 20"
            )
    
    def print_report(self):
        """Imprimir reporte final"""
        print("\n" + "=" * 60)
        print("📊 REPORTE FINAL")
        print("=" * 60)
        
        # Estado Nuclei
        print("\n🔧 Estado de Nuclei:")
        if self.results['nuclei_config'].get('installed'):
            print("   ✅ Instalado correctamente")
            print(f"   {self.results['nuclei_config'].get('version_output', '')}")
        else:
            print("   ❌ NO INSTALADO")
        
        # Conectividad
        print("\n🌐 Conectividad de Red:")
        if self.results['connectivity']:
            for host, status in self.results['connectivity'].items():
                emoji = "✅" if status else "❌"
                print(f"   {emoji} {host}")
        
        # Recomendaciones
        if self.results['recommendations']:
            print("\n💡 RECOMENDACIONES:")
            for i, rec in enumerate(self.results['recommendations'], 1):
                print(f"   {i}. {rec}")
        
        # Resumen
        print("\n📝 Resumen:")
        if self.results['nuclei_config'].get('installed') and \
           all(self.results['connectivity'].values()):
            print("   ✅ Todas las verificaciones pasaron.")
            print("   🚀 Sistema listo para escanear.")
        else:
            print("   ⚠️  Hay problemas que deben resolverse.")
            print("   📌 Sigue las recomendaciones de arriba.")
        
        print("\n" + "=" * 60)

def main():
    """Ejecutar diagnóstico"""
    diag = NucleiDiagnostic()
    diag.run_all_checks()
    
    # Guardar resultados
    report_file = Path("nuclei_diagnostic_report.json")
    with open(report_file, 'w') as f:
        json.dump(diag.results, f, indent=2)
    
    print(f"\n💾 Reporte guardado en: {report_file}")

if __name__ == "__main__":
    main()
