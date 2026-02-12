# Solución de Errores de Nuclei

## Errores Solucionados

### 1. ⚠️ "[WRN] The concurrency value is higher than max-host-error"

**Causa:** Usar concurrencia de 50 threads con pocas URLs causa conflicto entre threads.

**Solución implementada:**
- Reducida concurrencia de `50` a `20` threads
- Añadido parámetro `-max-host-error 20` para permitir 20 errores antes de cancelar
- Añadido `-rate-limit 100` para limitar requests por segundo

```bash
# ❌ ANTES (problemas)
nuclei -l targets.txt -c 50 -timeout 10 -retries 1

# ✅ DESPUÉS (optimizado)
nuclei -l targets.txt -c 20 -timeout 15 -retries 2 -max-host-error 20 -rate-limit 100
```

### 2. 🌐 "Failed to establish a new connection: [Errno 101] Network is unreachable"

**Causa:** Fallos de conectividad de red sin reintentos automáticos.

**Solución implementada:**
- Reintentos automáticos (hasta 3 intentos) para errores de conexión
- Delays incrementales entre reintentos (5s, 10s, 15s)
- Detección automática de errores de conexión vs otros errores

```python
# ✅ Reintentos automáticos activados
retry_count = 0
while retry_count < max_retries:
    try:
        # ejecutar nuclei...
    except ConnectionError:  # Reintentar
        retry_count += 1
        time.sleep(5 * retry_count)
```

## Configuraciones Recomendadas

### Para conexiones lentas o inestables:

Edita el comando nuclei y usa:
```bash
nuclei -l targets.txt \
  -c 10 \
  -timeout 20 \
  -retries 3 \
  -max-host-error 15 \
  -rate-limit 50
```

### Para conexiones rápidas y estables:

```bash
nuclei -l targets.txt \
  -c 30 \
  -timeout 10 \
  -retries 2 \
  -max-host-error 30 \
  -rate-limit 150
```

### Para redes restrictivas (proxies, firewalls):

```bash
nuclei -l targets.txt \
  -c 5 \
  -timeout 25 \
  -retries 3 \
  -max-host-error 5 \
  -rate-limit 30 \
  -headless
```

## Tabla de Parámetros

| Parámetro | Función | Valor Recomendado | Rango |
|---|---|---|---|
| `-c` | Concurrencia (threads) | 20 | 5-50 |
| `-timeout` | Timeout en segundos | 15 | 10-30 |
| `-retries` | Reintentos por host | 2 | 1-3 |
| `-max-host-error` | Max errores antes de cancelar | 20 | 5-50 |
| `-rate-limit` | Requests/segundo | 100 | 30-200 |

## Diagnóstico

### Verificar conectividad básica:

```powershell
# Test de DNS
Resolve-DnsName google.com

# Test de ping
Test-Connection -ComputerName 8.8.8.8

# Test de puerto
Test-NetConnection -ComputerName example.com -Port 443
```

### Ejecutar Nuclei manualmente:

```bash
# Test simple
nuclei -u https://example.com -s critical,high

# Test con debug
nuclei -u https://example.com -s critical,high -v

# Test con JSON output
nuclei -u https://example.com -jsonl -o results.json
```

### Verificar configuración de Nuclei:

```bash
nuclei -version
nuclei -h | grep -i "concurrency\|timeout\|retry"
```

## Archivos Modificados

✅ **shadow_scan.py** (línea ~264)
- Función `run_nuclei()` con reintentos automáticos
- Configuración optimizada de Nuclei

✅ **direct_scan.py** (línea ~108)
- Bloque de Nuclei con reintentos automáticos
- Parámetros sincronizados

## Próximos Pasos

1. **Prueba los cambios:**
   ```bash
   python shadow_scan.py -d example.com
   ```

2. **Si aún hay errores:**
   - Verificar conectividad con `ping` y `nslookup`
   - Reducir `-c` a 5-10 si hay muchos errores
   - Aumentar `-timeout` a 20-25
   - Revisar logs con `-v` (verbose)

3. **Para máxima flexibilidad:**
   - Edita los archivos Python y cambia los valores en `cmd = [...]`
   - Experimenta con valores según tu conexión

## Soporte

Si persisten los errores:

```bash
# Activar modo verbose
nuclei -u https://example.com -s critical,high -v

# Guardar logs completos
nuclei -u https://example.com -s critical,high 2>&1 | Tee-Object -FilePath nuclei.log

# Verificar versión y compatibilidad
nuclei -version
go version
```

---

**Última actualización:** Febrero 2026
**Versión:** Shadow-Scan v2.0+
