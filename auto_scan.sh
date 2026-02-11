#!/bin/bash
#
# Shadow-Scan - Script de Escaneo Automático
# Para usar con cron o programación automatizada
#

# Configuración
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Directorio de logs
LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"

# Timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/scan_$TIMESTAMP.log"

# Lista de dominios a escanear (uno por línea)
TARGETS_FILE="$SCRIPT_DIR/targets.txt"

# Función de logging
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Verificar que existe el archivo de targets
if [ ! -f "$TARGETS_FILE" ]; then
    log "⚠️  Creando archivo de targets de ejemplo..."
    cat > "$TARGETS_FILE" << EOF
# Lista de dominios a escanear
# Un dominio por línea, las líneas que empiezan con # son comentarios
#
# Ejemplo:
# example.com
# target.com
# company.com
EOF
    log "✅ Archivo creado en: $TARGETS_FILE"
    log "📝 Edita el archivo y agrega tus dominios"
    exit 0
fi

# Iniciar escaneo
log "🚀 Iniciando Shadow-Scan automático"
log "📁 Directorio: $SCRIPT_DIR"
log "📄 Log: $LOG_FILE"

# Contador de escaneos
SCANNED=0
FAILED=0

# Leer targets y escanear
while IFS= read -r domain || [ -n "$domain" ]; do
    # Ignorar líneas vacías y comentarios
    [[ -z "$domain" || "$domain" =~ ^[[:space:]]*# ]] && continue
    
    # Limpiar espacios
    domain=$(echo "$domain" | xargs)
    
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log "🎯 Escaneando: $domain"
    
    # Ejecutar escaneo
    if python3 "$SCRIPT_DIR/shadow_scan_full.py" \
        -d "$domain" \
        -s "critical,high,medium" \
        --telegram >> "$LOG_FILE" 2>&1; then
        
        log "✅ Escaneo completado: $domain"
        ((SCANNED++))
    else
        log "❌ Error escaneando: $domain"
        ((FAILED++))
    fi
    
    # Pausa entre escaneos (opcional)
    sleep 5
    
done < "$TARGETS_FILE"

# Resumen final
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log "📊 RESUMEN"
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log "✅ Exitosos: $SCANNED"
log "❌ Fallidos: $FAILED"
log "📄 Log completo: $LOG_FILE"
log "🏁 Escaneo automático finalizado"

# Limpiar logs antiguos (mantener últimos 30 días)
find "$LOG_DIR" -name "scan_*.log" -mtime +30 -delete

exit 0
