#!/usr/bin/env python3
"""
Quick Test - Verifica que los cambios se aplicaron correctamente
"""

import subprocess
from pathlib import Path

def verify_changes():
    """Verificar que los cambios se aplicaron"""
    
    print("✅ VERIFICANDO CAMBIOS")
    print("=" * 60)
    
    files_to_check = {
        'shadow_scan.py': [
            ("Concurrencia reducida a 20", "-c', '20"),
            ("Max host error añadido", "-max-host-error', '20"),
            ("Rate limit añadido", "-rate-limit', '100"),
            ("Reintentos automáticos", "max_retries = 3"),
        ],
        'direct_scan.py': [
            ("Concurrencia reducida a 20", "-c', '20"),
            ("Reintentos automáticos implementados", "while retry_count < max_retries"),
            ("Detección de errores de conexión", "Network is unreachable"),
        ],
        'NUCLEI_OPTIMIZATION.md': [
            ("Documentación de optimización creada", "Solución de Errores de Nuclei"),
        ],
        'nuclei_diagnostic.py': [
            ("Script de diagnóstico creado", "NucleiDiagnostic"),
        ],
        'NUCLEI_FIX_SUMMARY.md': [
            ("Resumen de cambios creado", "CAMBIOS IMPLEMENTADOS"),
        ],
    }
    
    all_ok = True
    
    for filename, checks in files_to_check.items():
        filepath = Path(filename)
        
        print(f"\n📄 {filename}")
        
        if not filepath.exists():
            print(f"   ❌ Archivo NO existe")
            all_ok = False
            continue
        
        content = filepath.read_text(encoding='utf-8', errors='ignore')
        
        for check_name, check_string in checks:
            if check_string.lower() in content.lower():
                print(f"   ✅ {check_name}")
            else:
                print(f"   ❌ {check_name}")
                all_ok = False
    
    print("\n" + "=" * 60)
    
    if all_ok:
        print("✅ TODOS LOS CAMBIOS SE APLICARON CORRECTAMENTE")
        print("\n🚀 Próximos pasos:")
        print("   1. python nuclei_diagnostic.py")
        print("   2. python shadow_scan.py -d example.com")
    else:
        print("⚠️  Algunos cambios no se aplicaron correctamente")
        print("   Revisa los detalles de arriba")
    
    print("=" * 60)

def test_nuclei():
    """Test básico de Nuclei"""
    print("\n🧪 TEST DE NUCLEI")
    print("=" * 60)
    
    try:
        result = subprocess.run(
            ['nuclei', '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print("✅ Nuclei instalado")
            print(f"   {result.stdout.strip()}")
        else:
            print("❌ Error ejecutando Nuclei")
            print(f"   {result.stderr}")
    except FileNotFoundError:
        print("❌ Nuclei NO está instalado")
        print("   Instálalo con: go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest")
    except Exception as e:
        print(f"⚠️  Error: {e}")
    
    print("=" * 60)

if __name__ == "__main__":
    verify_changes()
    test_nuclei()
    
    print("\n📋 VERIFICACIÓN COMPLETADA")
    print("Para diagnóstico completo ejecuta: python nuclei_diagnostic.py")
