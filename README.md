# 🕵️ Shadow-Scan

**Escáner Automatizado de Superficie de Ataque**

Sistema completo de reconocimiento (OSINT/Recon) que combina las mejores herramientas para mapear toda la superficie de ataque de una empresa y detectar vulnerabilidades críticas en minutos.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8+-blue)

## 🎯 Características

✅ **Pipeline Automatizado**: Subfinder → Httpx → Nuclei  
✅ **Notificaciones en Tiempo Real**: Alertas vía Telegram  
✅ **Dashboard Interactivo**: Panel web para visualizar resultados  
✅ **Base de Datos**: Histórico completo de escaneos  
✅ **Reportes JSON**: Exportación completa de datos  
✅ **Alertas Inteligentes**: Notificaciones solo para vulnerabilidades críticas  

## 🛠️ Stack Tecnológico

- **Subfinder**: Enumeración de subdominios
- **Httpx**: Verificación de hosts activos
- **Nuclei**: Escaneo de vulnerabilidades
- **Python**: Orquestación y lógica
- **Flask**: Dashboard web
- **SQLite**: Base de datos
- **Telegram Bot API**: Notificaciones

## 📋 Requisitos

- **Go**: 1.19 o superior
- **Python**: 3.8 o superior
- **Git**: Para clonar el repositorio

## 🚀 Instalación Rápida

```bash
# 1. Clonar repositorio (o descargar archivos)
git clone https://github.com/Davidgammer/shadow-scan.git
cd shadow-scan

# 2. Ejecutar instalación automatizada
chmod +x install.sh
./install.sh
```

### Instalación Manual

Si prefieres instalar manualmente:

```bash
# Instalar herramientas Go
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

# Actualizar templates de Nuclei
nuclei -update-templates

# Instalar dependencias Python
pip3 install -r requirements.txt
```

## 📱 Configuración de Telegram (Opcional)

Para recibir notificaciones en tiempo real:

### 1. Crear Bot de Telegram

1. Abre Telegram y busca `@BotFather`
2. Envía `/newbot` y sigue las instrucciones
3. Guarda el **token** que te proporciona

### 2. Obtener Chat ID

1. Envía un mensaje a tu nuevo bot
2. Visita: `https://api.telegram.org/bot<TU_TOKEN>/getUpdates`
3. Busca el campo `"chat":{"id":123456789}`
4. Ese número es tu **chat_id**

### 3. Configurar Shadow-Scan

**Opción A - Archivo de configuración:**
```bash
python3 shadow_scan_full.py --init-telegram
# Edita .telegram_config.json con tus credenciales
```

**Opción B - Variables de entorno:**
```bash
export TELEGRAM_BOT_TOKEN="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
export TELEGRAM_CHAT_ID="123456789"
```

## 🎮 Uso

### Escaneo Básico

```bash
# Escaneo simple
python3 shadow_scan.py -d example.com

# Con severidad personalizada
python3 shadow_scan.py -d example.com -s critical,high

# Con directorio de salida personalizado
python3 shadow_scan.py -d example.com -o my_scans
```

### Escaneo con Notificaciones Telegram

```bash
# Activar notificaciones Telegram
python3 shadow_scan_full.py -d example.com --telegram

# Escaneo completo con notificaciones
python3 shadow_scan_full.py -d example.com -s critical,high,medium --telegram
```

### Iniciar Dashboard

```bash
# Iniciar servidor web
python3 dashboard.py

# Acceder en: http://localhost:5000
```

Una vez en el dashboard:
1. Haz clic en "📥 Importar Escaneos"
2. Ingresa el directorio: `scan_results`
3. Visualiza todos tus escaneos

## 📊 Estructura de Salida

```
scan_results/
└── example.com_20240210_143025/
    ├── full_report.json          # Reporte completo
    ├── subdomains.txt             # Lista de subdominios
    ├── alive_hosts.json           # Hosts activos (httpx)
    ├── vulnerabilities.json       # Vulnerabilidades (nuclei)
    ├── targets.txt                # Targets para httpx
    └── nuclei_targets.txt         # Targets para nuclei
```

### Estructura del Reporte JSON

```json
{
  "scan_info": {
    "target": "example.com",
    "timestamp": "2024-02-10T14:30:25",
    "scan_directory": "scan_results/example.com_20240210_143025"
  },
  "statistics": {
    "total_subdomains": 45,
    "total_alive_hosts": 23,
    "total_vulnerabilities": 8,
    "vulnerability_severity": {
      "critical": 2,
      "high": 3,
      "medium": 3
    },
    "technologies_found": ["nginx", "cloudflare", "wordpress"]
  },
  "subdomains": [...],
  "alive_hosts": [...],
  "vulnerabilities": [...]
}
```

## 🔔 Notificaciones Telegram

Shadow-Scan envía las siguientes notificaciones:

1. **Inicio de Escaneo**: Confirma que el escaneo comenzó
2. **Progreso por Etapa**: Actualizaciones de subfinder, httpx, nuclei
3. **Resumen Completo**: Estadísticas finales del escaneo
4. **Alertas Críticas**: Vulnerabilidades de alta/crítica severidad
5. **Reporte JSON**: Archivo completo para descarga

### Ejemplo de Alerta

```
🚨 ALERTA: VULNERABILIDADES CRÍTICAS

⚠️ Se detectaron 5 vulnerabilidades de alta severidad

━━━━━━━━━━━━━━━━━━━━

🔴 1. SQL Injection
   🌐 Host: admin.example.com
   ⚠️  Severidad: CRITICAL

🟠 2. XSS Reflected
   🌐 Host: app.example.com
   ⚠️  Severidad: HIGH

... y 3 vulnerabilidades más
```

## 📈 Dashboard Web

El dashboard proporciona:

- **Estadísticas Globales**: Total de escaneos, vulnerabilidades, etc.
- **Gráficos Interactivos**: Visualización por severidad y timeline
- **Historial Completo**: Todos los escaneos realizados
- **Detalles por Escaneo**: Vista detallada de cada vulnerabilidad
- **Importación Masiva**: Cargar múltiples escaneos a la vez

### Características del Dashboard

- 🎨 Interfaz oscura moderna
- 📊 Gráficos con Chart.js
- 🔍 Filtrado y búsqueda
- 💾 Base de datos SQLite
- 📱 Responsive design

## 🔒 Consideraciones de Seguridad

⚠️ **IMPORTANTE**:

1. **Autorización**: Solo escanea dominios que tienes permiso para analizar
2. **Rate Limiting**: Ajusta los threads según sea necesario
3. **Credenciales**: Nunca subas tus tokens de Telegram a repositorios públicos
4. **Legal**: Asegúrate de cumplir con las leyes locales de ciberseguridad

## 🎯 Casos de Uso

### Bug Bounty
```bash
# Escaneo rápido de subdominios para bug hunting
python3 shadow_scan_full.py -d target.com -s critical,high --telegram
```

### Red Team
```bash
# Reconocimiento completo con todas las severidades
python3 shadow_scan_full.py -d client.com -s critical,high,medium,low
```

### Monitoreo Continuo
```bash
# Script cron para escaneos automáticos
0 2 * * * cd /path/to/shadow-scan && python3 shadow_scan_full.py -d mycompany.com --telegram
```

## 🛡️ Mejores Prácticas

1. **Escaneos Programados**: Usa cron para escaneos regulares
2. **Múltiples Targets**: Crea scripts para escanear múltiples dominios
3. **Filtrado Inteligente**: Ajusta severidades según tus necesidades
4. **Backup de Reportes**: Guarda los JSON en almacenamiento seguro
5. **Análisis de Tendencias**: Usa el dashboard para identificar patrones

## 📚 Comandos Útiles

```bash
# Ver ayuda
python3 shadow_scan_full.py --help

# Probar conexión con Telegram
python3 telegram_notifier.py

# Inicializar config de Telegram
python3 shadow_scan_full.py --init-telegram

# Importar escaneos al dashboard
python3 dashboard.py
# Luego en navegador: Importar → scan_results
```

## 🐛 Troubleshooting

### Error: "Herramientas faltantes"
```bash
# Reinstalar herramientas
./install.sh
```

### Error: "No module named 'flask'"
```bash
pip3 install -r requirements.txt
```

### Error: Timeout en nuclei
```bash
# Ajusta el timeout en shadow_scan.py línea 180
'-timeout', '30'  # Aumentar a 30 segundos
```

### Error: Telegram no envía mensajes
```bash
# Verificar token y chat_id
python3 telegram_notifier.py
```

## 🔧 Personalización

### Modificar Threads

Edita `shadow_scan.py`:

```python
# Httpx (línea 114)
'-threads', '100',  # Aumentar para escaneos más rápidos

# Nuclei (línea 179)
'-c', '100',  # Aumentar concurrencia
```

### Cambiar Templates de Nuclei

```python
# Agregar templates específicos
cmd = [
    'nuclei',
    '-l', str(targets_file),
    '-t', '/path/to/custom-templates/',  # Templates personalizados
    '-severity', severity,
    ...
]
```

### Agregar Más Notificaciones

Edita `telegram_notifier.py` para crear tus propias notificaciones personalizadas.

## 📊 Estadísticas de Rendimiento

Tiempos aproximados (dependen de la red y tamaño del target):

- **Subfinder**: 1-5 minutos
- **Httpx**: 2-10 minutos
- **Nuclei**: 5-30 minutos

**Total**: ~10-45 minutos por dominio

## 🤝 Contribuciones

Las contribuciones son bienvenidas:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 To-Do

- [ ] Integración con Discord webhooks
- [ ] Soporte para múltiples targets en un solo comando
- [ ] Export a PDF de reportes
- [ ] Integración con Slack
- [ ] API REST para el dashboard
- [ ] Modo stealth (escaneos más lentos pero discretos)
- [ ] Machine Learning para priorización de vulnerabilidades

## 📄 Licencia

MIT License - Ver archivo `LICENSE` para más detalles

## 👥 Autor

Creado con ❤️ para la comunidad de seguridad

## 🙏 Agradecimientos

- [ProjectDiscovery](https://projectdiscovery.io/) por las herramientas increíbles
- Comunidad de Bug Bounty
- Todos los contribuidores

## ⚡ Quick Start (TL;DR)

```bash
# Instalación
./install.sh

# Configurar Telegram (opcional)
python3 shadow_scan_full.py --init-telegram
# Editar .telegram_config.json

# Escanear
python3 shadow_scan_full.py -d example.com --telegram

# Ver resultados
python3 dashboard.py
# Abrir: http://localhost:5000
```

## 📞 Soporte

¿Problemas? Abre un issue en GitHub o contacta:

- 📧 Email:d4dot@proton.me
- 🐦 Twitter: @shadowscan
- 💬 Discord: ShadowScan Community

---

**⚠️ Disclaimer**: Esta herramienta es solo para propósitos educativos y de seguridad legítima. El uso no autorizado está prohibido y puede ser ilegal.

**Happy Hunting! 🎯**
