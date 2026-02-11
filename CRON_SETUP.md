# Configuración de Escaneos Automáticos

## 🕐 Configuración de Cron

### Editar Crontab

```bash
crontab -e
```

### Ejemplos de Programación

```bash
# Escanear todos los días a las 2 AM
0 2 * * * cd /path/to/shadow-scan && ./auto_scan.sh

# Escanear cada 6 horas
0 */6 * * * cd /path/to/shadow-scan && ./auto_scan.sh

# Escanear de lunes a viernes a las 9 AM
0 9 * * 1-5 cd /path/to/shadow-scan && ./auto_scan.sh

# Escanear el primer día del mes a las 3 AM
0 3 1 * * cd /path/to/shadow-scan && ./auto_scan.sh

# Escanear un dominio específico cada hora
0 * * * * cd /path/to/shadow-scan && python3 shadow_scan_full.py -d example.com --telegram
```

## 📝 Formato de Cron

```
┌───────────── minuto (0 - 59)
│ ┌───────────── hora (0 - 23)
│ │ ┌───────────── día del mes (1 - 31)
│ │ │ ┌───────────── mes (1 - 12)
│ │ │ │ ┌───────────── día de la semana (0 - 6) (Domingo=0)
│ │ │ │ │
* * * * * comando a ejecutar
```

## 🎯 Configuración de Targets

Edita `targets.txt` con tus dominios:

```bash
# Mis dominios a escanear
example.com
mycompany.com
client1.com
client2.com

# Dominios de bug bounty
hackerone.com
bugcrowd.com
```

## 📧 Notificaciones por Email (Opcional)

Añade al final de tu cron:

```bash
0 2 * * * cd /path/to/shadow-scan && ./auto_scan.sh 2>&1 | mail -s "Shadow-Scan Report" your@email.com
```

## 🔔 Verificar Logs

```bash
# Ver últimos logs
tail -f logs/scan_*.log

# Ver logs de hoy
cat logs/scan_$(date +%Y%m%d)*.log

# Buscar errores
grep "ERROR\|❌" logs/*.log
```

## ⚙️ Variables de Entorno

Crea un archivo `.env` en el directorio:

```bash
# Telegram
export TELEGRAM_BOT_TOKEN="your_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"

# Nuclei
export NUCLEI_TEMPLATES_PATH="/custom/path/to/templates"

# Configuración
export SCAN_SEVERITY="critical,high,medium"
export SCAN_OUTPUT_DIR="scan_results"
```

Carga en tu cron:

```bash
0 2 * * * cd /path/to/shadow-scan && source .env && ./auto_scan.sh
```

## 🛡️ Mejores Prácticas

1. **Testing**: Prueba tu configuración antes de automatizar
   ```bash
   ./auto_scan.sh
   ```

2. **Backups**: Respalda tus resultados regularmente
   ```bash
   # Cron para backup semanal
   0 0 * * 0 tar -czf backup_$(date +%Y%m%d).tar.gz scan_results/
   ```

3. **Monitoreo**: Revisa los logs periódicamente
   ```bash
   # Enviar resumen semanal
   0 9 * * 1 cd /path/to/shadow-scan && cat logs/scan_*.log | mail -s "Weekly Scan Summary" admin@company.com
   ```

4. **Rate Limiting**: No sobrecargues los servidores
   - Añade pausas entre escaneos
   - Ajusta threads en configuración
   - Distribuye escaneos a lo largo del día

## 🔍 Troubleshooting Cron

### Ver si cron está ejecutándose

```bash
# Ver logs de cron
grep CRON /var/log/syslog

# Ver último cron ejecutado
grep "shadow-scan" /var/log/syslog | tail -20
```

### Problemas comunes

**Error: command not found**
- Usa rutas absolutas en cron
- Verifica PATH: `which python3`

**Error: Permission denied**
- Verifica permisos: `chmod +x auto_scan.sh`
- Verifica ownership: `ls -la`

**Error: No output**
- Redirige output a archivo: `>> /tmp/cron.log 2>&1`
- Verifica que cron esté corriendo: `sudo service cron status`

## 📊 Monitoreo del Sistema

### Script de monitoreo simple

```bash
#!/bin/bash
# monitor.sh - Verifica que los escaneos estén funcionando

SCAN_DIR="/path/to/shadow-scan/scan_results"
ALERT_EMAIL="admin@company.com"

# Verificar si hay escaneos recientes (últimas 24 horas)
RECENT=$(find $SCAN_DIR -type d -mtime -1 | wc -l)

if [ $RECENT -eq 0 ]; then
    echo "⚠️ No hay escaneos en las últimas 24 horas" | mail -s "Shadow-Scan Alert" $ALERT_EMAIL
fi
```

Agregar a cron:
```bash
0 10 * * * /path/to/monitor.sh
```

## 🚀 Ejemplo Completo

```bash
# Archivo: /etc/cron.d/shadow-scan

# Variables
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=admin@company.com

# Escaneos programados
0 2 * * * user cd /opt/shadow-scan && ./auto_scan.sh
0 */6 * * * user cd /opt/shadow-scan && python3 shadow_scan_full.py -d priority-target.com --telegram

# Backup semanal
0 3 * * 0 user cd /opt/shadow-scan && tar -czf /backups/shadow-scan_$(date +\%Y\%m\%d).tar.gz scan_results/

# Monitoreo
0 10 * * * user /opt/shadow-scan/monitor.sh
```

## 📱 Integración con Otros Servicios

### Slack Webhook

```bash
# Enviar a Slack después del escaneo
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Shadow-Scan completed for example.com"}' \
  YOUR_SLACK_WEBHOOK_URL
```

### PagerDuty

```bash
# Alerta en PagerDuty si hay vulnerabilidades críticas
if grep -q "critical" scan_results/*/vulnerabilities.json; then
    # Trigger PagerDuty incident
fi
```

## 🎯 Tips de Optimización

1. **Distribuir carga**: Escanea diferentes dominios en diferentes horarios
2. **Priorizar**: Escanea dominios críticos con más frecuencia
3. **Recursos**: Ajusta threads según capacidad del servidor
4. **Almacenamiento**: Limpia resultados antiguos automáticamente

## 📚 Recursos Adicionales

- [Crontab Guru](https://crontab.guru) - Generador de expresiones cron
- [Cron Job Monitoring](https://cronitor.io) - Monitoreo de cron jobs
- ProjectDiscovery Docs - Documentación de las herramientas
