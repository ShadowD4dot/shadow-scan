# 📖 Shadow-Scan - Ejemplos de Uso

## 🎯 Casos de Uso Reales

### 1. Bug Bounty Hunter

**Escenario**: Estás participando en un programa de bug bounty y necesitas mapear rápidamente la superficie de ataque.

```bash
# Escaneo inicial rápido
python3 shadow_scan_full.py -d target.com -s critical,high --telegram

# Revisar resultados en dashboard
python3 dashboard.py

# Escaneo profundo de subdominios interesantes
python3 shadow_scan_full.py -d api.target.com -s critical,high,medium,low
```

**Flujo de trabajo recomendado**:
1. Escaneo rápido de dominio principal
2. Revisar subdominios en dashboard
3. Escaneo profundo de subdominios prometedores
4. Documentar vulnerabilidades encontradas

---

### 2. Red Team Assessment

**Escenario**: Evaluación de seguridad completa para un cliente.

```bash
# Día 1: Reconocimiento inicial
python3 shadow_scan_full.py -d client.com -s critical,high,medium

# Días 2-5: Escaneos programados
# Editar targets.txt con subdominios descubiertos
cat >> targets.txt << EOF
api.client.com
admin.client.com
portal.client.com
dev.client.com
EOF

# Ejecutar escaneos automáticos
./auto_scan.sh

# Generar reporte final
python3 dashboard.py
# Exportar resultados desde el dashboard
```

---

### 3. Monitoreo Continuo de Seguridad

**Escenario**: Monitorear continuamente tus propios activos digitales.

```bash
# Configurar cron para escaneos diarios
crontab -e
# Agregar: 0 2 * * * cd /opt/shadow-scan && ./auto_scan.sh

# Targets para monitoreo
cat > targets.txt << EOF
mycompany.com
app.mycompany.com
api.mycompany.com
EOF

# Las alertas se enviarán a Telegram automáticamente
```

---

### 4. Auditoría de Adquisición

**Escenario**: Due diligence técnica antes de adquirir una empresa.

```bash
# Escaneo exhaustivo
python3 shadow_scan_full.py -d targetacquisition.com -s critical,high,medium,low

# Análisis de resultados
python3 dashboard.py

# Generar reporte para stakeholders
# Los resultados JSON se pueden procesar para reportes ejecutivos
```

---

## 💡 Técnicas Avanzadas

### Escaneo de Múltiples Dominios

```bash
# Crear script personalizado
cat > scan_multiple.sh << 'EOF'
#!/bin/bash
DOMAINS=("example1.com" "example2.com" "example3.com")

for domain in "${DOMAINS[@]}"; do
    echo "Escaneando $domain..."
    python3 shadow_scan_full.py -d "$domain" --telegram
    sleep 300  # Pausa de 5 minutos entre escaneos
done
EOF

chmod +x scan_multiple.sh
./scan_multiple.sh
```

---

### Filtrado de Vulnerabilidades Específicas

```python
# filter_vulns.py - Script para filtrar vulnerabilidades
import json
import sys

def filter_critical_sqli(report_path):
    """Filtrar solo SQLi críticas"""
    with open(report_path) as f:
        report = json.load(f)
    
    sqli_vulns = [
        v for v in report['vulnerabilities']
        if 'sqli' in v['info'].get('tags', [])
        and v['info']['severity'] == 'critical'
    ]
    
    print(f"Found {len(sqli_vulns)} critical SQL injection vulnerabilities:")
    for vuln in sqli_vulns:
        print(f"  - {vuln['host']}: {vuln['info']['name']}")

if __name__ == "__main__":
    filter_critical_sqli(sys.argv[1])
```

Uso:
```bash
python3 filter_vulns.py scan_results/example.com_*/full_report.json
```

---

### Integración con Jira

```python
# jira_integration.py - Crear tickets en Jira automáticamente
import json
import requests
from pathlib import Path

JIRA_URL = "https://your-domain.atlassian.net"
JIRA_EMAIL = "your@email.com"
JIRA_API_TOKEN = "your_api_token"
PROJECT_KEY = "SEC"

def create_jira_ticket(vulnerability):
    """Crear ticket de Jira para una vulnerabilidad"""
    
    severity_priority = {
        'critical': 'Highest',
        'high': 'High',
        'medium': 'Medium',
        'low': 'Low'
    }
    
    issue_data = {
        "fields": {
            "project": {"key": PROJECT_KEY},
            "summary": f"[Security] {vulnerability['info']['name']}",
            "description": f"""
Host: {vulnerability['host']}
Severity: {vulnerability['info']['severity'].upper()}
Template: {vulnerability.get('template-id', 'N/A')}

Description:
{vulnerability['info'].get('description', 'No description')}

Matched at: {vulnerability.get('matched_at', 'N/A')}
            """,
            "issuetype": {"name": "Bug"},
            "priority": {"name": severity_priority.get(vulnerability['info']['severity'], 'Medium')}
        }
    }
    
    response = requests.post(
        f"{JIRA_URL}/rest/api/3/issue",
        auth=(JIRA_EMAIL, JIRA_API_TOKEN),
        json=issue_data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 201:
        issue_key = response.json()['key']
        print(f"✅ Created ticket: {issue_key}")
        return issue_key
    else:
        print(f"❌ Failed to create ticket: {response.text}")
        return None

def process_scan(report_path):
    """Procesar reporte y crear tickets para vulnerabilidades críticas/altas"""
    with open(report_path) as f:
        report = json.load(f)
    
    critical_vulns = [
        v for v in report['vulnerabilities']
        if v['info']['severity'] in ['critical', 'high']
    ]
    
    print(f"Creating {len(critical_vulns)} Jira tickets...")
    
    for vuln in critical_vulns:
        create_jira_ticket(vuln)

if __name__ == "__main__":
    import sys
    process_scan(sys.argv[1])
```

---

### Comparación de Escaneos

```python
# compare_scans.py - Comparar dos escaneos
import json
import sys

def compare_scans(old_report, new_report):
    """Comparar dos escaneos y encontrar nuevas vulnerabilidades"""
    
    with open(old_report) as f:
        old = json.load(f)
    
    with open(new_report) as f:
        new = json.load(f)
    
    # Crear sets de vulnerabilidades
    old_vulns = {
        (v['info']['name'], v['host'])
        for v in old['vulnerabilities']
    }
    
    new_vulns = {
        (v['info']['name'], v['host'])
        for v in new['vulnerabilities']
    }
    
    # Encontrar diferencias
    added = new_vulns - old_vulns
    removed = old_vulns - new_vulns
    
    print(f"📊 Comparación de Escaneos")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"🆕 Nuevas vulnerabilidades: {len(added)}")
    for name, host in sorted(added):
        print(f"   + {name} @ {host}")
    
    print(f"\n✅ Vulnerabilidades resueltas: {len(removed)}")
    for name, host in sorted(removed):
        print(f"   - {name} @ {host}")
    
    # Estadísticas
    old_stats = old['statistics']
    new_stats = new['statistics']
    
    print(f"\n📈 Cambios en Métricas:")
    print(f"   Subdominios: {old_stats['total_subdomains']} → {new_stats['total_subdomains']}")
    print(f"   Hosts activos: {old_stats['total_alive_hosts']} → {new_stats['total_alive_hosts']}")
    print(f"   Vulnerabilidades: {old_stats['total_vulnerabilities']} → {new_stats['total_vulnerabilities']}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 compare_scans.py old_report.json new_report.json")
        sys.exit(1)
    
    compare_scans(sys.argv[1], sys.argv[2])
```

---

## 🔧 Configuraciones Especializadas

### Alta Velocidad (Máxima Concurrencia)

```bash
# Editar shadow_scan.py y ajustar:
# - httpx threads: 200
# - nuclei concurrency: 100

# Usar solo severidades críticas
python3 shadow_scan_full.py -d target.com -s critical
```

### Modo Stealth (Bajo Perfil)

```bash
# Editar shadow_scan.py y ajustar:
# - httpx threads: 10
# - nuclei concurrency: 5
# - timeouts más largos

# Añadir pausas entre requests
# Distribuir escaneo a lo largo del día con cron
```

### Solo Reconocimiento (Sin Nuclei)

```python
# quick_recon.py - Solo subfinder + httpx
from shadow_scan import ShadowScanner

scanner = ShadowScanner("target.com")
subdomains = scanner.run_subfinder()
alive_hosts = scanner.run_httpx(subdomains)
scanner.save_results()
```

---

## 📊 Análisis de Datos

### Exportar a CSV

```python
# export_csv.py
import json
import csv
import sys

def export_to_csv(report_path, output_csv):
    """Exportar vulnerabilidades a CSV"""
    
    with open(report_path) as f:
        report = json.load(f)
    
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Host', 'Vulnerability', 'Severity', 'Description'])
        
        for vuln in report['vulnerabilities']:
            writer.writerow([
                vuln['host'],
                vuln['info']['name'],
                vuln['info']['severity'],
                vuln['info'].get('description', '')
            ])
    
    print(f"✅ Exported to {output_csv}")

if __name__ == "__main__":
    export_to_csv(sys.argv[1], sys.argv[2])
```

---

### Generar Gráficos

```python
# visualize.py
import json
import matplotlib.pyplot as plt
from collections import Counter

def plot_severity_distribution(report_path):
    """Graficar distribución de severidades"""
    
    with open(report_path) as f:
        report = json.load(f)
    
    severities = [v['info']['severity'] for v in report['vulnerabilities']]
    severity_counts = Counter(severities)
    
    plt.figure(figsize=(10, 6))
    plt.bar(severity_counts.keys(), severity_counts.values())
    plt.title('Distribución de Vulnerabilidades por Severidad')
    plt.xlabel('Severidad')
    plt.ylabel('Cantidad')
    plt.savefig('severity_distribution.png')
    print("✅ Gráfico guardado en severity_distribution.png")

if __name__ == "__main__":
    import sys
    plot_severity_distribution(sys.argv[1])
```

---

## 🎓 Mejores Prácticas

### 1. Documentación de Hallazgos

Crea un template para documentar vulnerabilidades:

```markdown
## Vulnerabilidad: [NOMBRE]

**Severidad**: CRITICAL/HIGH/MEDIUM/LOW  
**Host Afectado**: https://example.com  
**Fecha Descubierta**: 2024-02-10

### Descripción
[Descripción detallada]

### Pasos para Reproducir
1. ...
2. ...
3. ...

### Impacto
[Impacto de la vulnerabilidad]

### Recomendación
[Cómo remediar]

### Evidencia
[Screenshots, logs, etc.]
```

---

### 2. Workflow de Remediación

```bash
# 1. Escaneo inicial
python3 shadow_scan_full.py -d target.com --telegram

# 2. Exportar vulnerabilidades críticas
python3 filter_vulns.py scan_results/target.com_*/full_report.json > critical.txt

# 3. Crear tickets (manual o automático con Jira)

# 4. Esperar remediación

# 5. Re-escanear
python3 shadow_scan_full.py -d target.com --telegram

# 6. Comparar resultados
python3 compare_scans.py old_report.json new_report.json
```

---

### 3. Reportes Ejecutivos

```python
# executive_report.py
import json
from datetime import datetime

def generate_executive_summary(report_path):
    """Generar resumen ejecutivo"""
    
    with open(report_path) as f:
        report = json.load(f)
    
    stats = report['statistics']
    
    summary = f"""
# EXECUTIVE SECURITY REPORT

**Organization**: {report['scan_info']['target']}
**Scan Date**: {datetime.now().strftime('%B %d, %Y')}

## Key Findings

- **Total Attack Surface**: {stats['total_alive_hosts']} active hosts discovered
- **Security Issues**: {stats['total_vulnerabilities']} vulnerabilities identified
- **Critical Risk**: {stats['vulnerability_severity'].get('critical', 0)} CRITICAL issues
- **High Risk**: {stats['vulnerability_severity'].get('high', 0)} HIGH issues

## Risk Assessment

{"🔴 CRITICAL - Immediate action required" if stats['vulnerability_severity'].get('critical', 0) > 0 else ""}
{"🟠 HIGH - Address within 30 days" if stats['vulnerability_severity'].get('high', 0) > 0 else ""}
{"🟡 MEDIUM - Address within 90 days" if stats['vulnerability_severity'].get('medium', 0) > 0 else ""}

## Recommendations

1. Prioritize remediation of critical vulnerabilities
2. Implement regular security scanning
3. Review and harden exposed services
4. Consider penetration testing for high-risk assets

## Next Steps

- [ ] Remediate critical vulnerabilities
- [ ] Schedule follow-up scan
- [ ] Update security policies
- [ ] Train development team
    """
    
    with open('executive_summary.md', 'w') as f:
        f.write(summary)
    
    print("✅ Executive summary generated: executive_summary.md")

if __name__ == "__main__":
    import sys
    generate_executive_summary(sys.argv[1])
```

---

## 🚀 Scripts de Productividad

### Escaneo Rápido

```bash
#!/bin/bash
# quick_scan.sh - Escaneo rápido con notificación

DOMAIN=$1

if [ -z "$DOMAIN" ]; then
    echo "Uso: ./quick_scan.sh domain.com"
    exit 1
fi

echo "🚀 Iniciando escaneo rápido de $DOMAIN..."
python3 shadow_scan_full.py -d "$DOMAIN" -s critical,high --telegram

echo "✅ Escaneo completado"
echo "📊 Abre el dashboard para ver resultados:"
echo "   python3 dashboard.py"
```

---

## 🎯 Conclusión

Shadow-Scan es una herramienta flexible que se adapta a múltiples escenarios. Los ejemplos anteriores muestran solo algunas de las posibilidades. ¡Experimenta y crea tus propios workflows!

Para más información, consulta:
- README.md - Documentación principal
- CRON_SETUP.md - Configuración de escaneos automáticos
- Código fuente - Personalización avanzada
