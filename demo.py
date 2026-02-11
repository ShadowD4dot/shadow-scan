#!/usr/bin/env python3
"""
Shadow-Scan Demo - Modo de Demostración
Simula un escaneo completo para testing sin ejecutar herramientas reales
"""

import json
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import random

# Importar el notificador de Telegram
try:
    from telegram_notifier import TelegramNotifier, TelegramConfig
except ImportError:
    TelegramNotifier = None
    print("⚠️  telegram_notifier.py no encontrado, modo demo sin Telegram")


class DemoScanner:
    """Escáner de demostración con datos simulados"""
    
    def __init__(self, target: str, output_dir: str = "demo_results"):
        self.target = target
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.scan_dir = self.output_dir / f"{target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.scan_dir.mkdir(exist_ok=True)
    
    def generate_demo_subdomains(self) -> list:
        """Generar subdominios de ejemplo"""
        prefixes = [
            'www', 'mail', 'blog', 'api', 'dev', 'staging', 'admin', 'app',
            'portal', 'support', 'help', 'docs', 'cdn', 'static', 'images',
            'shop', 'store', 'checkout', 'payment', 'secure', 'vpn',
            'ftp', 'smtp', 'imap', 'test', 'qa', 'beta', 'demo'
        ]
        
        # Generar entre 20 y 50 subdominios
        num_subs = random.randint(20, 50)
        subdomains = [f"{random.choice(prefixes)}.{self.target}" for _ in range(num_subs)]
        
        # Asegurar algunos subdominios únicos
        subdomains = list(set(subdomains))
        
        return subdomains
    
    def generate_demo_hosts(self, subdomains: list) -> list:
        """Generar hosts activos de ejemplo"""
        alive_hosts = []
        
        # 30-60% de los subdominios están activos
        num_alive = int(len(subdomains) * random.uniform(0.3, 0.6))
        active_subs = random.sample(subdomains, num_alive)
        
        technologies = [
            'nginx', 'apache', 'cloudflare', 'aws-alb', 'wordpress',
            'react', 'vue', 'angular', 'nodejs', 'php', 'python',
            'mysql', 'postgresql', 'redis', 'docker', 'kubernetes'
        ]
        
        status_codes = [200, 200, 200, 301, 302, 403, 404, 500]
        
        for subdomain in active_subs:
            scheme = random.choice(['http', 'https'])
            url = f"{scheme}://{subdomain}"
            
            host_data = {
                'url': url,
                'host': subdomain,
                'status_code': random.choice(status_codes),
                'content_length': random.randint(1000, 50000),
                'title': f"{subdomain.split('.')[0].title()} - {self.target.split('.')[0].title()}",
                'technologies': random.sample(technologies, random.randint(1, 4))
            }
            
            alive_hosts.append(host_data)
        
        return alive_hosts
    
    def generate_demo_vulnerabilities(self, hosts: list) -> list:
        """Generar vulnerabilidades de ejemplo"""
        vulnerabilities = []
        
        vuln_templates = [
            {
                'name': 'SQL Injection - Error Based',
                'severity': 'critical',
                'description': 'SQL injection vulnerability detected through error-based testing',
                'tags': ['sqli', 'injection', 'owasp-top-10']
            },
            {
                'name': 'Cross-Site Scripting (XSS) - Reflected',
                'severity': 'high',
                'description': 'Reflected XSS vulnerability allows execution of arbitrary JavaScript',
                'tags': ['xss', 'injection', 'owasp-top-10']
            },
            {
                'name': 'Remote Code Execution (RCE)',
                'severity': 'critical',
                'description': 'Unauthenticated remote code execution vulnerability',
                'tags': ['rce', 'critical', 'code-execution']
            },
            {
                'name': 'Local File Inclusion (LFI)',
                'severity': 'high',
                'description': 'Local file inclusion allows reading sensitive files',
                'tags': ['lfi', 'file-inclusion', 'disclosure']
            },
            {
                'name': 'Exposed Admin Panel',
                'severity': 'medium',
                'description': 'Administrative panel accessible without authentication',
                'tags': ['exposure', 'config', 'access-control']
            },
            {
                'name': 'SSL/TLS Weak Cipher Suites',
                'severity': 'medium',
                'description': 'Server supports weak SSL/TLS cipher suites',
                'tags': ['ssl', 'tls', 'cryptography']
            },
            {
                'name': 'Directory Listing Enabled',
                'severity': 'low',
                'description': 'Directory listing exposes file structure',
                'tags': ['disclosure', 'misconfiguration']
            },
            {
                'name': 'Open Redirect',
                'severity': 'medium',
                'description': 'Unvalidated redirect allows phishing attacks',
                'tags': ['redirect', 'phishing']
            }
        ]
        
        # Generar entre 5 y 15 vulnerabilidades
        num_vulns = random.randint(5, 15)
        
        for _ in range(num_vulns):
            host = random.choice(hosts)
            template = random.choice(vuln_templates)
            
            vuln = {
                'template-id': f"cve-{random.randint(2020, 2024)}-{random.randint(1000, 9999)}",
                'info': {
                    'name': template['name'],
                    'severity': template['severity'],
                    'description': template['description'],
                    'tags': template['tags']
                },
                'host': host['url'],
                'matched_at': f"{host['url']}/{random.choice(['admin', 'api', 'login', 'search', 'upload'])}",
                'timestamp': datetime.now().isoformat()
            }
            
            vulnerabilities.append(vuln)
        
        return vulnerabilities
    
    def run_demo_scan(self) -> dict:
        """Ejecutar escaneo de demostración"""
        
        print(f"\n{'='*60}")
        print(f"🕵️  SHADOW-SCAN DEMO - Modo Demostración")
        print(f"{'='*60}")
        print(f"🎯 Target: {self.target}")
        print(f"📁 Output: {self.scan_dir}")
        print(f"⚠️  MODO DEMO: Datos simulados")
        print(f"{'='*60}\n")
        
        # Simular subfinder
        print("🔍 [1/3] Simulando enumeración de subdominios...")
        import time
        time.sleep(1)
        subdomains = self.generate_demo_subdomains()
        print(f"   ✅ {len(subdomains)} subdominios generados")
        
        # Guardar subdominios
        with open(self.scan_dir / "subdomains.txt", 'w') as f:
            f.write('\n'.join(subdomains))
        
        # Simular httpx
        print("\n🌐 [2/3] Simulando verificación de hosts...")
        time.sleep(1)
        alive_hosts = self.generate_demo_hosts(subdomains)
        print(f"   ✅ {len(alive_hosts)} hosts activos detectados")
        
        # Guardar hosts activos
        with open(self.scan_dir / "alive_hosts.json", 'w') as f:
            for host in alive_hosts:
                f.write(json.dumps(host) + '\n')
        
        # Simular nuclei
        print("\n🎯 [3/3] Simulando escaneo de vulnerabilidades...")
        time.sleep(2)
        vulnerabilities = self.generate_demo_vulnerabilities(alive_hosts)
        
        # Estadísticas por severidad
        severity_counts = defaultdict(int)
        for vuln in vulnerabilities:
            sev = vuln['info']['severity']
            severity_counts[sev] += 1
        
        print(f"   ✅ {len(vulnerabilities)} vulnerabilidades generadas")
        for sev, count in sorted(severity_counts.items()):
            emoji = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}.get(sev, '⚪')
            print(f"      {emoji} {sev.upper()}: {count}")
        
        # Guardar vulnerabilidades
        with open(self.scan_dir / "vulnerabilities.json", 'w') as f:
            for vuln in vulnerabilities:
                f.write(json.dumps(vuln) + '\n')
        
        # Generar estadísticas
        technologies = set()
        for host in alive_hosts:
            technologies.update(host.get('technologies', []))
        
        stats = {
            'target': self.target,
            'total_subdomains': len(subdomains),
            'total_alive_hosts': len(alive_hosts),
            'total_vulnerabilities': len(vulnerabilities),
            'vulnerability_severity': dict(severity_counts),
            'technologies_found': list(technologies),
            'scan_time': datetime.now().isoformat()
        }
        
        # Crear reporte completo
        report = {
            'scan_info': {
                'target': self.target,
                'timestamp': datetime.now().isoformat(),
                'scan_directory': str(self.scan_dir),
                'mode': 'DEMO'
            },
            'statistics': stats,
            'subdomains': subdomains,
            'alive_hosts': alive_hosts,
            'vulnerabilities': vulnerabilities
        }
        
        # Guardar reporte
        report_file = self.scan_dir / "full_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Resumen
        print(f"\n{'='*60}")
        print("📊 RESUMEN EJECUTIVO")
        print(f"{'='*60}")
        print(f"🌐 Subdominios descubiertos: {stats['total_subdomains']}")
        print(f"✅ Hosts activos: {stats['total_alive_hosts']}")
        print(f"🎯 Vulnerabilidades totales: {stats['total_vulnerabilities']}")
        
        if stats['vulnerability_severity']:
            print(f"\n🔥 Desglose por severidad:")
            for sev in ['critical', 'high', 'medium', 'low']:
                if sev in stats['vulnerability_severity']:
                    count = stats['vulnerability_severity'][sev]
                    emoji = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}.get(sev, '⚪')
                    print(f"   {emoji} {sev.upper()}: {count}")
        
        print(f"\n💾 Reporte guardado en: {report_file}")
        print(f"{'='*60}\n")
        
        return {
            'report_path': str(report_file),
            'stats': stats,
            'report': report
        }


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Shadow-Scan Demo - Modo de Demostración',
        epilog="""
Ejemplos:
  python3 demo.py -d example.com
  python3 demo.py -d example.com --telegram
        """
    )
    
    parser.add_argument('-d', '--domain', required=True,
                       help='Dominio para demostración')
    parser.add_argument('--telegram', action='store_true',
                       help='Enviar notificaciones de demo a Telegram')
    
    args = parser.parse_args()
    
    # Crear escáner de demo
    scanner = DemoScanner(args.domain)
    
    # Configurar Telegram si está habilitado
    telegram = None
    if args.telegram and TelegramNotifier:
        telegram = TelegramConfig.from_env() or TelegramConfig.from_file()
        
        if telegram:
            telegram.send_message(
                "🎭 <b>SHADOW-SCAN DEMO</b>\n\n"
                f"🎯 Target: <code>{args.domain}</code>\n"
                "⚠️ Modo demostración con datos simulados"
            )
    
    # Ejecutar escaneo de demo
    results = scanner.run_demo_scan()
    
    # Enviar notificaciones
    if telegram:
        telegram.send_scan_complete(results['stats'])
        if results['report']['vulnerabilities']:
            telegram.send_critical_alert(results['report']['vulnerabilities'])
        telegram.send_full_report(results['report_path'])
    
    print("✅ Demo completada")
    print(f"\n💡 Próximos pasos:")
    print(f"   1. Importa estos resultados al dashboard:")
    print(f"      python3 dashboard.py")
    print(f"   2. Ejecuta un escaneo real:")
    print(f"      python3 shadow_scan_full.py -d {args.domain}\n")


if __name__ == "__main__":
    main()
