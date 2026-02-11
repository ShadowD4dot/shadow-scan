#!/usr/bin/env python3
"""
Telegram Notifier para Shadow-Scan
Envía reportes y alertas en tiempo real
"""

import requests
import json
from typing import List, Dict, Optional
from datetime import datetime
import os
from pathlib import Path


class TelegramNotifier:
    """Cliente de notificaciones Telegram"""
    
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
        self.max_message_length = 4096
        
    def send_message(self, message: str, parse_mode: str = "HTML") -> bool:
        """Enviar mensaje de texto"""
        try:
            # Dividir mensajes largos
            if len(message) > self.max_message_length:
                chunks = self._split_message(message)
                for chunk in chunks:
                    self._send_chunk(chunk, parse_mode)
            else:
                self._send_chunk(message, parse_mode)
            return True
        except Exception as e:
            print(f"❌ Error enviando mensaje: {e}")
            return False
    
    def _send_chunk(self, message: str, parse_mode: str):
        """Enviar un chunk de mensaje"""
        url = f"{self.api_url}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': parse_mode,
            'disable_web_page_preview': True
        }
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
    
    def _split_message(self, message: str) -> List[str]:
        """Dividir mensaje largo en chunks"""
        chunks = []
        lines = message.split('\n')
        current_chunk = ""
        
        for line in lines:
            if len(current_chunk) + len(line) + 1 < self.max_message_length:
                current_chunk += line + '\n'
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = line + '\n'
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def send_document(self, file_path: str, caption: str = "") -> bool:
        """Enviar archivo"""
        try:
            url = f"{self.api_url}/sendDocument"
            
            with open(file_path, 'rb') as f:
                files = {'document': f}
                data = {
                    'chat_id': self.chat_id,
                    'caption': caption
                }
                response = requests.post(url, data=data, files=files, timeout=30)
                response.raise_for_status()
            
            return True
        except Exception as e:
            print(f"❌ Error enviando documento: {e}")
            return False
    
    def send_scan_start(self, domain: str) -> bool:
        """Notificar inicio de escaneo"""
        message = f"""
🚀 <b>SHADOW-SCAN INICIADO</b>

🎯 <b>Target:</b> <code>{domain}</code>
⏰ <b>Hora:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🔄 Escaneo en progreso...
        """.strip()
        
        return self.send_message(message)
    
    def send_scan_complete(self, stats: Dict) -> bool:
        """Notificar finalización de escaneo con estadísticas"""
        
        # Emojis para severidad
        severity_emojis = {
            'critical': '🔴',
            'high': '🟠',
            'medium': '🟡',
            'low': '🟢',
            'info': '⚪'
        }
        
        message = f"""
✅ <b>ESCANEO COMPLETADO</b>

🎯 <b>Target:</b> <code>{stats.get('target', 'N/A')}</code>
⏰ <b>Finalizado:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 <b>RESULTADOS:</b>
━━━━━━━━━━━━━━━━━━━━
🌐 Subdominios: <b>{stats.get('total_subdomains', 0)}</b>
✅ Hosts activos: <b>{stats.get('total_alive_hosts', 0)}</b>
🎯 Vulnerabilidades: <b>{stats.get('total_vulnerabilities', 0)}</b>
        """.strip()
        
        # Añadir desglose de severidad
        vuln_severity = stats.get('vulnerability_severity', {})
        if vuln_severity:
            message += "\n\n🔥 <b>Por Severidad:</b>\n"
            severity_order = ['critical', 'high', 'medium', 'low', 'info']
            for sev in severity_order:
                if sev in vuln_severity:
                    count = vuln_severity[sev]
                    emoji = severity_emojis.get(sev, '⚪')
                    message += f"{emoji} <b>{sev.upper()}:</b> {count}\n"
        
        # Añadir tecnologías
        technologies = stats.get('technologies_found', [])
        if technologies:
            tech_preview = ', '.join(technologies[:5])
            if len(technologies) > 5:
                tech_preview += f" (+{len(technologies)-5} más)"
            message += f"\n🔧 <b>Tecnologías:</b> {tech_preview}"
        
        return self.send_message(message)
    
    def send_critical_alert(self, vulnerabilities: List[Dict]) -> bool:
        """Enviar alerta de vulnerabilidades críticas"""
        
        critical_vulns = [
            v for v in vulnerabilities 
            if v.get('info', {}).get('severity') in ['critical', 'high']
        ]
        
        if not critical_vulns:
            return True
        
        message = f"""
🚨 <b>ALERTA: VULNERABILIDADES CRÍTICAS</b>

⚠️ Se detectaron <b>{len(critical_vulns)}</b> vulnerabilidades de alta severidad

━━━━━━━━━━━━━━━━━━━━
        """.strip()
        
        # Mostrar primeras 5 vulnerabilidades
        for i, vuln in enumerate(critical_vulns[:5], 1):
            info = vuln.get('info', {})
            severity = info.get('severity', 'unknown').upper()
            name = info.get('name', 'Unknown')
            host = vuln.get('host', 'N/A')
            
            emoji = '🔴' if severity == 'CRITICAL' else '🟠'
            
            message += f"\n\n{emoji} <b>{i}. {name}</b>"
            message += f"\n   🌐 Host: <code>{host}</code>"
            message += f"\n   ⚠️  Severidad: <b>{severity}</b>"
            
            # Añadir descripción corta si existe
            description = info.get('description', '')
            if description and len(description) < 100:
                message += f"\n   📝 {description}"
        
        if len(critical_vulns) > 5:
            message += f"\n\n... y {len(critical_vulns) - 5} vulnerabilidades más"
        
        message += "\n\n🔍 Revisa el reporte completo para más detalles"
        
        return self.send_message(message)
    
    def send_full_report(self, report_path: str) -> bool:
        """Enviar reporte completo como documento"""
        if not os.path.exists(report_path):
            print(f"❌ Reporte no encontrado: {report_path}")
            return False
        
        caption = f"""
📄 Reporte Completo Shadow-Scan
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """.strip()
        
        return self.send_document(report_path, caption)
    
    def send_progress_update(self, stage: str, message: str) -> bool:
        """Enviar actualización de progreso"""
        
        stage_emojis = {
            'subfinder': '🔍',
            'httpx': '🌐',
            'nuclei': '🎯'
        }
        
        emoji = stage_emojis.get(stage.lower(), '🔄')
        
        notification = f"""
{emoji} <b>{stage.upper()}</b>

{message}
        """.strip()
        
        return self.send_message(notification)


class TelegramConfig:
    """Configuración de Telegram desde variables de entorno o archivo"""
    
    @staticmethod
    def from_env() -> Optional[TelegramNotifier]:
        """Crear notificador desde variables de entorno"""
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if bot_token and chat_id:
            return TelegramNotifier(bot_token, chat_id)
        
        return None
    
    @staticmethod
    def from_file(config_path: str = ".telegram_config.json") -> Optional[TelegramNotifier]:
        """Crear notificador desde archivo de configuración"""
        if not os.path.exists(config_path):
            return None
        
        try:
            with open(config_path) as f:
                config = json.load(f)
            
            bot_token = config.get('bot_token')
            chat_id = config.get('chat_id')
            
            if bot_token and chat_id:
                return TelegramNotifier(bot_token, chat_id)
        except Exception as e:
            print(f"❌ Error leyendo config: {e}")
        
        return None
    
    @staticmethod
    def create_config_template(output_path: str = ".telegram_config.json"):
        """Crear archivo de configuración template"""
        template = {
            "bot_token": "YOUR_BOT_TOKEN_HERE",
            "chat_id": "YOUR_CHAT_ID_HERE",
            "instructions": {
                "1": "Crea un bot con @BotFather en Telegram",
                "2": "Copia el token del bot",
                "3": "Envía un mensaje a tu bot",
                "4": "Obtén tu chat_id desde: https://api.telegram.org/botYOUR_TOKEN/getUpdates",
                "5": "Rellena los valores arriba"
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(template, f, indent=2)
        
        print(f"✅ Template creado en: {output_path}")
        print("📝 Edita el archivo con tus credenciales de Telegram")


# Testing
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        TelegramConfig.create_config_template()
        sys.exit(0)
    
    # Intentar cargar configuración
    notifier = TelegramConfig.from_env() or TelegramConfig.from_file()
    
    if not notifier:
        print("❌ No se encontró configuración de Telegram")
        print("💡 Ejecuta: python telegram_notifier.py init")
        print("   Luego edita .telegram_config.json con tus credenciales")
        sys.exit(1)
    
    # Test
    print("🧪 Probando conexión con Telegram...")
    if notifier.send_message("✅ <b>Shadow-Scan Test</b>\n\nConexión exitosa!"):
        print("✅ Mensaje enviado correctamente")
    else:
        print("❌ Error enviando mensaje")
