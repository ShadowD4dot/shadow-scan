# 🚀 Guía Rápida: 3 Pasos para Subir a GitHub

## ⚡ Método Automático (MÁS FÁCIL)

```bash
# En el directorio shadow-scan:
./setup_github.sh
```

El script te preguntará:
- Tu nombre
- Tu email  
- Tu usuario de GitHub
- Nombre del repositorio

Y preparará todo automáticamente! 🎉

---

## 📋 Método Manual

### Paso 1: Crear Repositorio en GitHub

1. Ve a: https://github.com/new
2. **Repository name**: `shadow-scan`
3. **Visibility**: Selecciona **🔒 Private**
4. ❌ NO marques nada más
5. Click **"Create repository"**

### Paso 2: Preparar tu Proyecto

```bash
cd /ruta/a/shadow-scan

# Crear .gitignore
cat > .gitignore << 'EOF'
__pycache__/
scan_results/
demo_results/
logs/
*.db
.telegram_config.json
.env
targets.txt
*.log
templates/
.vscode/
.DS_Store
EOF

# Inicializar git
git init
git add .
git commit -m "Initial commit: Shadow-Scan"
```

### Paso 3: Subir a GitHub

**Opción A - HTTPS (Simple):**
```bash
git remote add origin https://github.com/TU_USUARIO/shadow-scan.git
git branch -M main
git push -u origin main
```

**Opción B - GitHub CLI (Más Rápido):**
```bash
gh auth login
gh repo create shadow-scan --private --source=. --push
```

---

## ✅ Verificación

1. Abre: https://github.com/TU_USUARIO/shadow-scan
2. Debes ver el badge **🔒 Private**
3. Todos tus archivos deben estar ahí
4. Verifica que NO esté `.telegram_config.json`

---

## 🔄 Futuras Actualizaciones

```bash
# Hacer cambios...

git add .
git commit -m "Update: descripción del cambio"
git push
```

---

## 🆘 Problemas Comunes

**"Permission denied"**
```bash
# Generar SSH key
ssh-keygen -t ed25519 -C "tu@email.com"
# Agregar a GitHub: Settings → SSH Keys
```

**"Token required"**
- GitHub → Settings → Developer settings → Personal access tokens
- Generate token → Scope: `repo`
- Usa el token como password

**"Already exists"**
```bash
git remote remove origin
# Vuelve a agregar el remote
```

---

## 📚 Documentación Completa

Para más detalles, consulta:
- `GITHUB_GUIDE.md` - Guía completa paso a paso
- `setup_github.sh` - Script automático

---

## 💡 Tips de Seguridad

### ❌ NUNCA subas:
- `.telegram_config.json`
- `scan_results/`
- `logs/`
- `*.db`
- `targets.txt`

### ✅ SIEMPRE verifica:
```bash
git status
# Si ves archivos sensibles, añádelos a .gitignore
```

---

## 🎯 TL;DR (Resumen Ultra Rápido)

```bash
# 1. Ejecutar script automático
./setup_github.sh

# 2. Crear repo en https://github.com/new (PRIVATE)

# 3. Copiar y ejecutar los comandos que te muestra el script

# ¡Listo! 🎉
```
