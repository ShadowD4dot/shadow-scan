#!/usr/bin/env python3
"""
Shadow-Scan Full - Escáner Integrado con Notificaciones
Combina escaneo + Telegram + Dashboard
"""

import sys
import argparse
from pathlib import Path

# Importar módulos
from shadow_scan import ShadowScanner
from telegram_notifier import TelegramNotifier, TelegramConfig


class IntegratedScanner(ShadowScanner):
    """Escáner con notificaciones Telegram integradas"""
    
    def __init__(self, target: str, output_dir: str = "scan_results", 
                 telegram_notifier: TelegramNotifier = None):
        super().__init__(target, output_dir)
        self.telegram = telegram_notifier
    
    def run_full_scan(self, nuclei_severity: str = "critical,high,medium") -> dict:
        """Ejecutar escaneo completo con notificaciones"""
        
        # Notificar inicio
        if self.telegram:
            self.telegram.send_scan_start(self.target)
        
        print(f"\n{'='*60}")
        print(f"🕵️  SHADOW-SCAN - Análisis de Superficie de Ataque")
        print(f"{'='*60}")
        print(f"🎯 Target: {self.target}")
        print(f"📁 Output: {self.scan_dir}")
        if self.telegram:
            print(f"📱 Telegram: ✅ Habilitado")
        print(f"{'='*60}")
        
        # 1. Subfinder
        subdomains = self.run_subfinder()
        if self.telegram and subdomains:
            self.telegram.send_progress_update(
                'subfinder',
                f"✅ {len(subdomains)} subdominios encontrados"
            )
        
        # 2. Httpx
        alive_hosts = self.run_httpx(subdomains)
        if self.telegram and alive_hosts:
            self.telegram.send_progress_update(
                'httpx',
                f"✅ {len(alive_hosts)} hosts activos detectados"
            )
        
        # 3. Nuclei
        vulnerabilities = self.run_nuclei(alive_hosts, nuclei_severity)
        
        # 4. Guardar resultados
        report_path = self.save_results()
        
        # 5. Generar estadísticas
        stats = self.generate_stats()
        
        # 6. Notificaciones finales
        if self.telegram:
            # Enviar resumen
            self.telegram.send_scan_complete(stats)
            
            # Alertas de vulnerabilidades críticas
            if vulnerabilities:
                self.telegram.send_critical_alert(vulnerabilities)
            
            # Enviar reporte completo
            self.telegram.send_full_report(report_path)
        
        # 7. Mostrar resumen
        self.print_summary()
        
        return {
            'report_path': report_path,
            'stats': stats,
            'results': self.results
        }


def main():
    parser = argparse.ArgumentParser(
        description='Shadow-Scan Full - Escáner Automatizado con Notificaciones',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  # Escaneo básico
  %(prog)s -d example.com
  
  # Con notificaciones Telegram
  %(prog)s -d example.com --telegram
  
  # Severidad personalizada
  %(prog)s -d example.com -s critical,high --telegram
  
  # Configuración inicial de Telegram
  %(prog)s --init-telegram

Configuración de Telegram:
  1. Ejecuta: %(prog)s --init-telegram
  2. Edita .telegram_config.json con tus credenciales
  3. O configura variables de entorno:
     export TELEGRAM_BOT_TOKEN="your_token"
     export TELEGRAM_CHAT_ID="your_chat_id"
        """
    )
    
    parser.add_argument('-d', '--domain',
                       help='Dominio objetivo para escanear')
    parser.add_argument('-s', '--severity', 
                       default='critical,high,medium',
                       help='Severidades de Nuclei (default: critical,high,medium)')
    parser.add_argument('-o', '--output', 
                       default='scan_results',
                       help='Directorio de salida (default: scan_results)')
    parser.add_argument('--telegram', action='store_true',
                       help='Habilitar notificaciones Telegram')
    parser.add_argument('--init-telegram', action='store_true',
                       help='Crear archivo de configuración de Telegram')
    
    args = parser.parse_args()
    
    # Inicializar configuración de Telegram
    if args.init_telegram:
        TelegramConfig.create_config_template()
        return
    
    # Verificar que se proporcionó un dominio
    if not args.domain:
        parser.print_help()
        print("\n❌ Error: Se requiere especificar un dominio (-d/--domain)")
        sys.exit(1)
    
    # Configurar Telegram si está habilitado
    telegram = None
    if args.telegram:
        telegram = TelegramConfig.from_env() or TelegramConfig.from_file()
        
        if not telegram:
            print("\n⚠️  Notificaciones Telegram solicitadas pero no configuradas")
            print("💡 Ejecuta: python shadow_scan_full.py --init-telegram")
            print("   Luego edita .telegram_config.json con tus credenciales\n")
            
            response = input("¿Continuar sin Telegram? (s/n): ")
            if response.lower() != 's':
                sys.exit(1)
    
    # Crear escáner integrado
    scanner = IntegratedScanner(args.domain, args.output, telegram)
    
    # Verificar herramientas
    if not scanner.check_tools():
        sys.exit(1)
    
    # Ejecutar escaneo
    try:
        results = scanner.run_full_scan(args.severity)
        
        print(f"\n✅ Escaneo completado exitosamente")
        print(f"📄 Reporte: {results['report_path']}")
        
        if telegram:
            print(f"📱 Notificaciones enviadas a Telegram")
        
        print(f"\n💡 Para visualizar resultados:")
        print(f"   python dashboard.py")
        print(f"   Luego importa el directorio: {args.output}\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Escaneo interrumpido por el usuario")
        if telegram:
            telegram.send_message("⚠️ <b>Escaneo Interrumpido</b>\n\nEl escaneo fue cancelado por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error durante el escaneo: {e}")
        if telegram:
            telegram.send_message(f"❌ <b>Error en Escaneo</b>\n\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
