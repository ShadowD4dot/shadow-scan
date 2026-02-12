# 📝 Uso Correcto de Shadow-Scan

## ✅ Formatos de Dominio Aceptados

Shadow-Scan ahora acepta múltiples formatos y extrae automáticamente el dominio:

### Ejemplos Válidos:

```bash
# Solo dominio (RECOMENDADO)
python3 shadow_scan_full.py -d example.com

# Con subdominio
python3 shadow_scan_full.py -d api.example.com

# URL completa con HTTPS
python3 shadow_scan_full.py -d https://example.com

# URL completa con HTTP
python3 shadow_scan_full.py -d http://example.com

# URL con path (se ignora el path)
python3 shadow_scan_full.py -d https://example.com/login

# URL con puerto (se ignora el puerto)
python3 shadow_scan_full.py -d https://example.com:8080

# Combinaciones
python3 shadow_scan_full.py -d https://api.example.com/v1/endpoint
# → Se extrae: api.example.com
```

## 🎯 Tu Caso Específico

Tu comando original:
```bash
python3 shadow_scan_full.py -d https://egdp-dev.avangenio.net -s critical,high,medium --telegram
```

**Ahora funciona correctamente** ✅

El programa:
1. Detecta que es una URL completa
2. Extrae el dominio: `egdp-dev.avangenio.net`
3. Crea el directorio: `scan_results/egdp-dev.avangenio.net_20260211_154954/`

## 📁 Estructura de Directorios

Los nombres de directorios se sanitizan automáticamente:

```
scan_results/
├── example.com_20260211_120000/
├── api.example.com_20260211_130000/
├── egdp-dev.avangenio.net_20260211_140000/
└── subdomain.target.org_20260211_150000/
```

Caracteres problemáticos (`:`, `/`, `\`, etc.) se reemplazan por `_`

## 🚀 Comandos Listos para Usar

### Escaneo Básico
```bash
# Forma más simple
python3 shadow_scan_full.py -d egdp-dev.avangenio.net --telegram

# Con URL completa (también funciona)
python3 shadow_scan_full.py -d https://egdp-dev.avangenio.net --telegram
```

### Escaneo con Severidades Específicas
```bash
# Solo críticas y altas
python3 shadow_scan_full.py -d egdp-dev.avangenio.net -s critical,high --telegram

# Incluir medium
python3 shadow_scan_full.py -d egdp-dev.avangenio.net -s critical,high,medium --telegram

# Todas las severidades
python3 shadow_scan_full.py -d egdp-dev.avangenio.net -s critical,high,medium,low --telegram
```

### Escaneo sin Telegram
```bash
# Sin notificaciones
python3 shadow_scan_full.py -d egdp-dev.avangenio.net -s critical,high
```

### Escaneo con Output Personalizado
```bash
# Directorio de salida personalizado
python3 shadow_scan_full.py -d egdp-dev.avangenio.net -o mis_escaneos --telegram
```

## 🧪 Modo Demo (Para Testing)

```bash
# Probar sin herramientas reales
python3 demo.py -d egdp-dev.avangenio.net

# Demo con Telegram
python3 demo.py -d egdp-dev.avangenio.net --telegram
```

## 💡 Mejores Prácticas

### 1. Usa Solo el Dominio (Más Limpio)
```bash
# Mejor
python3 shadow_scan_full.py -d egdp-dev.avangenio.net

# También funciona, pero innecesario
python3 shadow_scan_full.py -d https://egdp-dev.avangenio.net
```

### 2. Severidades Según el Objetivo

**Bug Bounty / Pentesting:**
```bash
python3 shadow_scan_full.py -d target.com -s critical,high --telegram
```

**Auditoría Completa:**
```bash
python3 shadow_scan_full.py -d target.com -s critical,high,medium,low
```

**Escaneo Rápido:**
```bash
python3 shadow_scan_full.py -d target.com -s critical
```

### 3. Organización de Resultados

```bash
# Un directorio por proyecto
python3 shadow_scan_full.py -d client1.com -o scans/client1

# Fechas en el nombre
python3 shadow_scan_full.py -d target.com -o scans/$(date +%Y%m%d)
```

## 🔍 Verificar Resultados

```bash
# Ver últimos escaneos
ls -lht scan_results/ | head

# Ver estructura de un escaneo
tree scan_results/egdp-dev.avangenio.net_*/

# Ver reporte JSON
cat scan_results/egdp-dev.avangenio.net_*/full_report.json | jq .

# Contar vulnerabilidades por severidad
cat scan_results/*/vulnerabilities.json | jq -r '.info.severity' | sort | uniq -c
```

## 📊 Múltiples Dominios

### Opción 1: Secuencial
```bash
python3 shadow_scan_full.py -d domain1.com --telegram
python3 shadow_scan_full.py -d domain2.com --telegram
python3 shadow_scan_full.py -d domain3.com --telegram
```

### Opción 2: Script
```bash
# Crear targets.txt
cat > targets.txt << EOF
egdp-dev.avangenio.net
api.avangenio.net
portal.avangenio.net
EOF

# Ejecutar auto_scan.sh
./auto_scan.sh
```

### Opción 3: Loop
```bash
for domain in domain1.com domain2.com domain3.com; do
    python3 shadow_scan_full.py -d $domain --telegram
    sleep 300  # Pausa de 5 minutos entre escaneos
done
```

## ⚙️ Variables de Entorno (Opcional)

```bash
# Configurar Telegram permanentemente
export TELEGRAM_BOT_TOKEN="your_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"

# Ahora solo necesitas:
python3 shadow_scan_full.py -d target.com --telegram
```

## 🐛 Troubleshooting

### Error: "No such file or directory"
**Causa**: Versión antigua del script sin soporte para URLs

**Solución**: Ya está arreglado en la nueva versión ✅

### Error: "Tool not found"
**Solución**:
```bash
./install.sh
```

### Error: Telegram no envía
**Solución**:
```bash
python3 shadow_scan_full.py --init-telegram
# Editar .telegram_config.json
```

## 📖 Ayuda Completa

```bash
# Ver todas las opciones
python3 shadow_scan_full.py --help

# Ver versión
python3 shadow_scan.py --version  # (si lo implementamos)
```

## 🎯 Tu Comando Correcto

Basado en tu caso:

```bash
# RECOMENDADO (sin https://)
python3 shadow_scan_full.py -d egdp-dev.avangenio.net -s critical,high,medium --telegram

# TAMBIÉN FUNCIONA (con https://)
python3 shadow_scan_full.py -d https://egdp-dev.avangenio.net -s critical,high,medium --telegram
```

Ambos funcionan idénticamente. El programa extrae `egdp-dev.avangenio.net` automáticamente.

## 📝 Próximos Pasos

1. **Ejecuta el escaneo**:
   ```bash
   python3 shadow_scan_full.py -d egdp-dev.avangenio.net --telegram
   ```

2. **Espera los resultados** (10-45 minutos típicamente)

3. **Revisa en el dashboard**:
   ```bash
   python3 dashboard.py
   # Abre: http://localhost:5000
   ```

4. **Importa los resultados** en el dashboard:
   - Click "📥 Importar Escaneos"
   - Directorio: `scan_results`

¡Listo! 🎉
