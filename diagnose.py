#!/usr/bin/env python3
"""
Script de diagnóstico para Shadow-Scan
Verifica configuración y prueba las herramientas
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"\n🔍 {description}")
    print(f"   Comando: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        
        if result.returncode == 0:
            output = result.stdout.strip()
            if output:
                print(f"   ✅ Salida:\n{output[:500]}")
            else:
                print(f"   ⚠️  Sin salida (puede ser normal)")
            return True
        else:
            print(f"   ❌ Error: {result.stderr[:200]}")
            return False
    except subprocess.TimeoutExpired:
        print(f"   ⚠️  Timeout (30s)")
        return False
    except Exception as e:
        print(f"   ❌ Excepción: {e}")
        return False

def main():
    print("="*60)
    print("🔬 SHADOW-SCAN - Diagnóstico del Sistema")
    print("="*60)
    
    # 1. Verificar herramientas
    print("\n📦 VERIFICACIÓN DE HERRAMIENTAS")
    print("-"*60)
    
    tools = {
        'subfinder': ['subfinder', '-version'],
        'httpx': ['httpx', '-version'],
        'nuclei': ['nuclei', '-version']
    }
    
    tools_ok = True
    for tool, cmd in tools.items():
        if run_command(cmd, f"Verificando {tool}"):
            print(f"   ✅ {tool} instalado")
        else:
            print(f"   ❌ {tool} NO encontrado")
            tools_ok = False
    
    if not tools_ok:
        print("\n⚠️  Algunas herramientas faltan. Ejecuta: ./install.sh")
        return
    
    # 2. Test de Subfinder con dominio conocido
    print("\n🧪 TEST DE SUBFINDER")
    print("-"*60)
    
    test_domains = [
        'google.com',  # Debe encontrar muchos
        'example.com',  # Debe encontrar algunos
    ]
    
    for domain in test_domains:
        print(f"\n📡 Probando: {domain}")
        result = subprocess.run(
            ['subfinder', '-d', domain, '-silent'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        subdomains = result.stdout.strip().split('\n')
        subdomains = [s for s in subdomains if s]
        
        print(f"   Encontrados: {len(subdomains)} subdominios")
        if len(subdomains) > 0:
            print(f"   Ejemplos: {subdomains[:3]}")
        else:
            print(f"   ⚠️  No se encontraron subdominios")
    
    # 3. Test con el dominio del usuario
    print("\n🎯 TEST CON TU DOMINIO")
    print("-"*60)
    
    target = "egdp-dev.avangenio.net"
    print(f"\n📡 Escaneando: {target}")
    
    # Prueba 1: Subfinder básico
    print("\n   1️⃣ Subfinder básico:")
    result = subprocess.run(
        ['subfinder', '-d', target, '-silent'],
        capture_output=True,
        text=True,
        timeout=60
    )
    basic_subs = result.stdout.strip().split('\n')
    basic_subs = [s for s in basic_subs if s]
    print(f"      Encontrados: {len(basic_subs)}")
    
    # Prueba 2: Subfinder con todas las fuentes
    print("\n   2️⃣ Subfinder con todas las fuentes:")
    result = subprocess.run(
        ['subfinder', '-d', target, '-all', '-silent'],
        capture_output=True,
        text=True,
        timeout=120
    )
    all_subs = result.stdout.strip().split('\n')
    all_subs = [s for s in all_subs if s]
    print(f"      Encontrados: {len(all_subs)}")
    if all_subs:
        print(f"      Ejemplos: {all_subs[:5]}")
    
    # Prueba 3: Verificar si el dominio principal existe
    print("\n   3️⃣ Verificando dominio principal con httpx:")
    result = subprocess.run(
        ['httpx', '-u', f'https://{target}', '-silent'],
        capture_output=True,
        text=True,
        timeout=30
    )
    if result.stdout.strip():
        print(f"      ✅ Dominio accesible: {result.stdout.strip()}")
    else:
        print(f"      ⚠️  Dominio no responde o no es accesible")
    
    # 4. Diagnóstico de configuración de Subfinder
    print("\n⚚️ CONFIGURACIÓN DE SUBFINDER")
    print("-"*60)
    
    config_path = Path.home() / '.config' / 'subfinder' / 'provider-config.yaml'
    
    if config_path.exists():
        print(f"   ✅ Archivo de config existe: {config_path}")
        with open(config_path) as f:
            print(f"   Primeras líneas:\n{f.read(200)}")
    else:
        print(f"   ⚠️  No hay archivo de configuración")
        print(f"   💡 Subfinder funciona sin config pero encuentra menos resultados")
        print(f"\n   Para mejorar resultados, configura APIs gratuitas:")
        print(f"   1. Crea el archivo: {config_path}")
        print(f"   2. Agrega tus API keys (ver documentación de Subfinder)")
    
    # 5. Soluciones sugeridas
    print("\n💡 SOLUCIONES SUGERIDAS")
    print("-"*60)
    
    if len(all_subs) == 0:
        print("""
   El dominio 'egdp-dev.avangenio.net' parece no tener subdominios públicos
   descubiertos por las fuentes de Subfinder.
   
   Posibles razones:
   
   1. ✅ Es un dominio de desarrollo/staging privado
      → Puede que realmente no tenga subdominios públicos
      
   2. ⚠️  El dominio está detrás de protecciones (Cloudflare, etc.)
      → Configura APIs en Subfinder para mejores resultados
      
   3. 💡 Puedes crear una lista manual de targets:
   
      # Crear archivo con dominios/subdominios conocidos
      cat > targets_manual.txt << 'EOF'
egdp-dev.avangenio.net
api.egdp-dev.avangenio.net
portal.egdp-dev.avangenio.net
admin.egdp-dev.avangenio.net
EOF
      
      # Ejecutar directamente httpx y nuclei:
      httpx -l targets_manual.txt -o alive.txt
      nuclei -l alive.txt -s critical,high,medium
   
   4. 🔧 Alternativa: Escanear directamente el dominio principal
      
      # Sin subfinder, solo el dominio principal
      echo "egdp-dev.avangenio.net" > single_target.txt
      httpx -l single_target.txt -json -o httpx_result.json
      nuclei -u https://egdp-dev.avangenio.net -s critical,high,medium
        """)
    else:
        print(f"\n   ✅ Subfinder encontró {len(all_subs)} subdominios")
        print(f"   El escaneo debería funcionar correctamente")
    
    print("\n" + "="*60)
    print("✅ Diagnóstico completado")
    print("="*60)

if __name__ == "__main__":
    main()
