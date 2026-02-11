# 🕵️ Shadow-Scan - Estructura del Proyecto

## 📁 Estructura de Archivos

```
shadow-scan/
├── 📄 README.md                    # Documentación principal
├── 📄 EXAMPLES.md                  # Ejemplos de uso y casos reales
├── 📄 CRON_SETUP.md               # Configuración de escaneos automáticos
├── 📄 requirements.txt             # Dependencias Python
│
├── 🔧 Scripts Principales
│   ├── shadow_scan.py              # Motor principal del escáner
│   ├── shadow_scan_full.py         # Versión con notificaciones Telegram
│   ├── telegram_notifier.py        # Cliente de Telegram
│   └── dashboard.py                # Panel web interactivo
│
├── 🛠️ Utilidades
│   ├── install.sh                  # Script de instalación automática
│   ├── auto_scan.sh               # Escaneos automáticos programados
│   └── demo.py                     # Demostración con datos simulados
│
└── 📂 Generados en ejecución
    ├── scan_results/               # Resultados de escaneos
    ├── demo_results/               # Resultados de demos
    ├── logs/                       # Logs de escaneos automáticos
    ├── templates/                  # Templates HTML del dashboard
    ├── scans.db                    # Base de datos SQLite
    ├── targets.txt                 # Lista de dominios a escanear
    └── .telegram_config.json       # Configuración de Telegram
```

## 🚀 Inicio Rápido

### Opción 1: Instalación Completa (Recomendada)

```bash
# 1. Verificar requisitos
go version    # Debe ser 1.19+
python3 --version  # Debe ser 3.8+

# 2. Instalar todo automáticamente
chmod +x install.sh
./install.sh

# 3. Configurar Telegram (opcional)
python3 shadow_scan_full.py --init-telegram
# Editar .telegram_config.json con tus credenciales

# 4. Probar con demo
python3 demo.py -d example.com

# 5. Escaneo real
python3 shadow_scan_full.py -d example.com --telegram

# 6. Ver resultados
python3 dashboard.py
# Abrir: http://localhost:5000
```

### Opción 2: Solo Testing (Sin Instalación)

```bash
# Ejecutar demo sin instalar herramientas
python3 demo.py -d example.com

# Ver resultados
python3 dashboard.py
```

### Opción 3: Instalación Manual

```bash
# 1. Instalar herramientas Go
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

# 2. Actualizar templates
nuclei -update-templates

# 3. Instalar dependencias Python
pip3 install -r requirements.txt

# 4. Listo para usar
python3 shadow_scan.py -d example.com
```

## 📊 Componentes del Sistema

### 1. Motor de Escaneo (`shadow_scan.py`)

**Función**: Orquestación del pipeline de herramientas

**Flujo**:
```
Input: Dominio objetivo
    ↓
[Subfinder] → Enumerar subdominios
    ↓
[Httpx] → Verificar hosts activos
    ↓
[Nuclei] → Detectar vulnerabilidades
    ↓
Output: Reporte JSON completo
```

**Características**:
- ✅ Manejo de errores y timeouts
- ✅ Logs detallados de progreso
- ✅ Estadísticas en tiempo real
- ✅ Exportación JSON estructurada

---

### 2. Sistema de Notificaciones (`telegram_notifier.py`)

**Función**: Alertas en tiempo real vía Telegram

**Tipos de Notificaciones**:
1. 🚀 Inicio de escaneo
2. 🔄 Progreso por etapa
3. ✅ Resumen completo
4. 🚨 Alertas críticas
5. 📄 Reporte completo (archivo)

**Configuración**:
- Variables de entorno o archivo JSON
- Soporte para mensajes largos (auto-split)
- Formato HTML con emojis

---

### 3. Dashboard Web (`dashboard.py`)

**Función**: Visualización interactiva de resultados

**Características**:
- 📊 Gráficos de Chart.js
- 🗄️ Base de datos SQLite
- 🔍 Vista detallada por escaneo
- 📥 Importación masiva
- 📱 Diseño responsive

**API Endpoints**:
- `GET /api/scans` - Listar todos los escaneos
- `GET /api/scan/<id>` - Detalles de escaneo
- `GET /api/statistics` - Estadísticas globales
- `POST /api/import_scan` - Importar escaneo
- `POST /api/import_from_directory` - Importación masiva

---

### 4. Escáner Integrado (`shadow_scan_full.py`)

**Función**: Combina escaneo + Telegram en un solo comando

**Uso**:
```bash
python3 shadow_scan_full.py -d target.com --telegram
```

**Ventajas**:
- Todo en un solo comando
- Notificaciones automáticas
- Configuración simplificada

---

### 5. Demo (`demo.py`)

**Función**: Simulación sin herramientas reales

**Uso**:
```bash
python3 demo.py -d example.com
```

**Características**:
- Datos realistas simulados
- Mismo formato de salida
- Perfecto para testing
- Compatible con dashboard

---

### 6. Escaneos Automáticos (`auto_scan.sh`)

**Función**: Orquestación de múltiples targets

**Configuración**:
```bash
# 1. Editar targets.txt
cat > targets.txt << EOF
example.com
target1.com
target2.com
EOF

# 2. Ejecutar
./auto_scan.sh

# 3. Programar con cron
0 2 * * * cd /path/to/shadow-scan && ./auto_scan.sh
```

**Características**:
- Logs detallados
- Manejo de errores
- Pausas configurables
- Limpieza automática

---

## 🔧 Configuración Detallada

### Telegram

**Método 1 - Variables de Entorno**:
```bash
export TELEGRAM_BOT_TOKEN="your_token"
export TELEGRAM_CHAT_ID="your_chat_id"
```

**Método 2 - Archivo JSON**:
```bash
python3 shadow_scan_full.py --init-telegram
# Editar .telegram_config.json
```

### Dashboard

**Puerto y Host**:
```python
# Editar dashboard.py línea final:
app.run(host='0.0.0.0', port=5000)
```

**Base de Datos**:
```python
# Cambiar ubicación de BD:
db = ScanDatabase("custom_path/scans.db")
```

### Severidades de Nuclei

```bash
# Solo críticas
-s critical

# Críticas y altas
-s critical,high

# Todas
-s critical,high,medium,low,info
```

### Threads y Concurrencia

**Httpx** (shadow_scan.py línea ~114):
```python
'-threads', '50',  # Aumentar para más velocidad
```

**Nuclei** (shadow_scan.py línea ~179):
```python
'-c', '50',  # Aumentar concurrencia
```

---

## 📈 Flujos de Trabajo

### Workflow 1: Bug Bounty

```
1. Escaneo inicial rápido
   └─→ python3 shadow_scan_full.py -d target.com -s critical,high

2. Revisar en dashboard
   └─→ python3 dashboard.py

3. Escaneo profundo de subdominios interesantes
   └─→ python3 shadow_scan.py -d api.target.com -s critical,high,medium

4. Documentar y reportar hallazgos
```

### Workflow 2: Monitoreo Continuo

```
1. Configurar targets
   └─→ Editar targets.txt

2. Programar cron
   └─→ 0 2 * * * /path/to/auto_scan.sh

3. Recibir alertas automáticas
   └─→ Telegram notifica vulnerabilidades

4. Revisar dashboard periódicamente
   └─→ Análisis de tendencias
```

### Workflow 3: Auditoría Completa

```
1. Reconocimiento inicial
   └─→ Escaneo completo con todas las severidades

2. Análisis de resultados
   └─→ Dashboard + Exportación CSV

3. Remediación
   └─→ Crear tickets, asignar, resolver

4. Verificación
   └─→ Re-escaneo + Comparación

5. Reporteo
   └─→ Generar reporte ejecutivo
```

---

## 🎯 Casos de Uso por Perfil

### 🎓 Pentester Junior
- **Usar**: `shadow_scan.py` para aprender el flujo
- **Severidad**: `critical,high`
- **Frecuencia**: Manual, bajo demanda

### 👨‍💻 Pentester Senior
- **Usar**: `shadow_scan_full.py` con Telegram
- **Severidad**: `critical,high,medium`
- **Frecuencia**: Programado con cron

### 🏢 Security Team
- **Usar**: Pipeline completo con dashboard
- **Severidad**: Todas
- **Frecuencia**: Monitoreo continuo 24/7
- **Extra**: Integración con Jira/Slack

### 🐛 Bug Bounty Hunter
- **Usar**: Scripts personalizados + demo
- **Severidad**: `critical,high`
- **Frecuencia**: Por programa
- **Extra**: Múltiples targets, comparación

---

## 🔒 Seguridad y Mejores Prácticas

### ✅ Hacer

- Obtener autorización antes de escanear
- Usar rate limiting apropiado
- Documentar todos los hallazgos
- Mantener logs seguros
- Actualizar templates regularmente
- Usar VPN/proxy cuando sea apropiado

### ❌ No Hacer

- Escanear sin permiso
- Subir tokens a GitHub
- Ejecutar con máxima velocidad en producción
- Ignorar false positives
- Compartir resultados sin autorización

---

## 🆘 Troubleshooting

### Problema: "Tool not found"
**Solución**: Ejecutar `./install.sh` o instalar manualmente

### Problema: "Permission denied"
**Solución**: `chmod +x *.sh`

### Problema: Telegram no funciona
**Solución**: Verificar token y chat_id con `python3 telegram_notifier.py`

### Problema: Dashboard vacío
**Solución**: Importar escaneos desde el botón "📥 Importar"

### Problema: Timeout en Nuclei
**Solución**: Aumentar timeout en configuración o reducir concurrencia

---

## 📚 Referencias

### Herramientas Utilizadas
- [Subfinder](https://github.com/projectdiscovery/subfinder)
- [Httpx](https://github.com/projectdiscovery/httpx)
- [Nuclei](https://github.com/projectdiscovery/nuclei)

### Documentación
- [ProjectDiscovery Docs](https://docs.projectdiscovery.io/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Flask Documentation](https://flask.palletsprojects.com/)

### Recursos Adicionales
- OWASP Top 10
- Bug Bounty Platforms (HackerOne, Bugcrowd)
- CVE Database

---

## 🎓 Próximos Pasos

Una vez que domines Shadow-Scan:

1. **Personalización**: Modifica los scripts para tus necesidades
2. **Integración**: Conecta con tus herramientas favoritas
3. **Automatización**: Crea workflows complejos
4. **Contribución**: Comparte mejoras con la comunidad

---

## 📞 Soporte

¿Preguntas? ¿Problemas? ¿Sugerencias?

- 📖 Lee la documentación completa en README.md
- 💡 Revisa los ejemplos en EXAMPLES.md
- 🔧 Configura cron con CRON_SETUP.md
- 🐛 Abre un issue en GitHub

---

**Happy Hunting! 🎯**

*Shadow-Scan - Tu aliado en reconocimiento automatizado*
