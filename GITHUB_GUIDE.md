# 🔒 Guía: Subir Shadow-Scan a GitHub Privado

## 📋 Requisitos Previos

- Cuenta de GitHub
- Git instalado en tu sistema
- Terminal/línea de comandos

## 🚀 Método 1: Interfaz Web de GitHub (Más Fácil)

### Paso 1: Crear Repositorio Privado en GitHub

1. Ve a https://github.com/new
2. Configura el repositorio:
   - **Repository name**: `shadow-scan` (o el nombre que prefieras)
   - **Description**: `Automated Attack Surface Scanner with Telegram notifications`
   - **Visibility**: Selecciona **🔒 Private**
   - ❌ **NO** marques "Add a README file"
   - ❌ **NO** marques "Add .gitignore"
   - ❌ **NO** marques "Choose a license"
3. Haz clic en **"Create repository"**

### Paso 2: Preparar tu Proyecto Local

```bash
# Navegar al directorio del proyecto
cd /ruta/donde/descargaste/shadow-scan

# Inicializar git
git init

# Crear .gitignore para excluir archivos sensibles
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# Resultados de escaneos (NO subir a GitHub)
scan_results/
demo_results/
logs/
*.db
scans.db

# Configuración sensible (IMPORTANTE)
.telegram_config.json
.env
*.key
*.pem

# Archivos temporales
targets.txt
*.log
templates/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
EOF

# Agregar todos los archivos
git add .

# Primer commit
git commit -m "Initial commit: Shadow-Scan - Automated Attack Surface Scanner"
```

### Paso 3: Conectar con GitHub

```bash
# Reemplaza TU_USUARIO con tu nombre de usuario de GitHub
git remote add origin https://github.com/TU_USUARIO/shadow-scan.git

# Verificar que se agregó correctamente
git remote -v

# Subir el código
git branch -M main
git push -u origin main
```

Si te pide credenciales, ingresa:
- **Username**: Tu usuario de GitHub
- **Password**: Tu **Personal Access Token** (no tu contraseña normal)

---

## 🔑 Método 2: Usando SSH (Recomendado para Uso Frecuente)

### Paso 1: Generar SSH Key (si no tienes una)

```bash
# Generar nueva SSH key
ssh-keygen -t ed25519 -C "tu_email@example.com"

# Presiona Enter 3 veces (ubicación por defecto, sin passphrase)

# Copiar la clave pública
cat ~/.ssh/id_ed25519.pub
# Copia todo el contenido
```

### Paso 2: Agregar SSH Key a GitHub

1. Ve a GitHub → Settings → SSH and GPG keys
2. Clic en **"New SSH key"**
3. **Title**: `Mi Computadora` (o el nombre que prefieras)
4. **Key**: Pega la clave pública que copiaste
5. Clic en **"Add SSH key"**

### Paso 3: Crear y Conectar Repositorio

```bash
# Navegar al proyecto
cd /ruta/donde/descargaste/shadow-scan

# Inicializar git
git init

# Crear .gitignore (mismo que arriba)
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

# Agregar archivos
git add .
git commit -m "Initial commit: Shadow-Scan"

# Crear repositorio privado desde línea de comandos (requiere GitHub CLI)
# O créalo manualmente en https://github.com/new

# Conectar con SSH
git remote add origin git@github.com:TU_USUARIO/shadow-scan.git

# Subir
git branch -M main
git push -u origin main
```

---

## 🔐 Método 3: Usando GitHub CLI (gh)

```bash
# Instalar GitHub CLI
# Ubuntu/Debian
sudo apt install gh

# macOS
brew install gh

# Autenticarse
gh auth login
# Selecciona: GitHub.com → HTTPS → Login with a web browser

# Navegar al proyecto
cd /ruta/donde/descargaste/shadow-scan

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
EOF

# Crear repositorio privado directamente
gh repo create shadow-scan --private --source=. --remote=origin --push

# ¡Listo! Ya está en GitHub
```

---

## ⚠️ IMPORTANTE: Seguridad

### ❌ NUNCA Subas Estos Archivos

```
.telegram_config.json    # Contiene tu token de bot
.env                      # Variables de entorno
targets.txt               # Puede contener info sensible
scan_results/             # Resultados de escaneos
logs/                     # Logs con info sensible
*.db                      # Base de datos con resultados
```

### ✅ Verificar .gitignore

```bash
# Verificar que git está ignorando archivos sensibles
git status

# Si aparece .telegram_config.json, ¡DETENTE!
# Agrégalo a .gitignore antes de hacer commit
```

### 🛡️ Si Subiste Archivos Sensibles por Error

```bash
# Eliminar archivo del historial de git
git rm --cached .telegram_config.json
git commit -m "Remove sensitive config file"
git push

# Regenerar tokens/credenciales comprometidas
# - Crear nuevo bot de Telegram
# - Cambiar cualquier credential expuesta
```

---

## 📝 Configuración del README en GitHub

Después de subir, edita el README.md para agregar tu badge de repositorio privado:

```markdown
# 🕵️ Shadow-Scan

![Private](https://img.shields.io/badge/status-private-red)
![Python](https://img.shields.io/badge/python-3.8+-blue)

[Resto de tu README...]
```

---

## 🔄 Actualizaciones Futuras

Cuando hagas cambios al proyecto:

```bash
# Ver cambios
git status

# Agregar cambios
git add .

# Commit con mensaje descriptivo
git commit -m "Add: Nueva funcionalidad X"

# Subir a GitHub
git push
```

### Mensajes de Commit Recomendados

```bash
git commit -m "Add: Nueva funcionalidad de X"
git commit -m "Fix: Corrección de bug en Y"
git commit -m "Update: Mejora en módulo Z"
git commit -m "Docs: Actualización de documentación"
git commit -m "Refactor: Reorganización de código"
```

---

## 👥 Compartir con Colaboradores

Si quieres dar acceso a otros usuarios:

1. Ve a tu repositorio en GitHub
2. Settings → Collaborators → Add people
3. Ingresa el username de GitHub
4. Selecciona el nivel de permiso (Read, Write, Admin)

---

## 📦 Clonar en Otra Máquina

```bash
# Con HTTPS
git clone https://github.com/TU_USUARIO/shadow-scan.git

# Con SSH
git clone git@github.com:TU_USUARIO/shadow-scan.git

# Entrar al directorio
cd shadow-scan

# Instalar
./install.sh
```

---

## 🔍 Verificar que es Privado

1. Abre tu repositorio en GitHub
2. Deberías ver un badge **🔒 Private** junto al nombre
3. Intenta acceder desde una ventana de incógnito sin login
4. Deberías recibir un error 404 (No encontrado)

---

## 💡 Tips Adicionales

### Crear Token de Acceso Personal (PAT)

Si usas HTTPS y te pide password:

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. Scopes: Marca `repo` (acceso completo a repositorios privados)
4. Generate token
5. **Copia el token** (solo se muestra una vez)
6. Usa este token como password cuando git te lo pida

### Usar Múltiples Repositorios

```bash
# Agregar otro remote (por ejemplo, backup en GitLab)
git remote add gitlab git@gitlab.com:TU_USUARIO/shadow-scan.git

# Ver todos los remotes
git remote -v

# Push a ambos
git push origin main
git push gitlab main
```

### Crear Branches para Desarrollo

```bash
# Crear branch para nueva feature
git checkout -b feature/telegram-discord

# Trabajar en la feature...

# Hacer commit
git add .
git commit -m "Add: Discord notifications"

# Subir branch
git push -u origin feature/telegram-discord

# En GitHub, crear Pull Request para merge
```

---

## 🆘 Solución de Problemas

### Error: "remote origin already exists"

```bash
git remote remove origin
git remote add origin https://github.com/TU_USUARIO/shadow-scan.git
```

### Error: "Permission denied (publickey)"

```bash
# Verificar SSH key
ssh -T git@github.com

# Si falla, regenerar SSH key y agregarla a GitHub
```

### Error: "Updates were rejected"

```bash
# Forzar push (CUIDADO: sobrescribe el remoto)
git push -f origin main

# O hacer pull primero
git pull origin main --allow-unrelated-histories
git push origin main
```

### Ver Historial de Commits

```bash
git log --oneline --graph --all
```

---

## ✅ Checklist Final

- [ ] Repositorio creado en GitHub como **Private**
- [ ] .gitignore configurado correctamente
- [ ] NO subiste .telegram_config.json
- [ ] NO subiste scan_results/
- [ ] NO subiste logs/
- [ ] Código subido exitosamente
- [ ] README.md visible en GitHub
- [ ] Badge de Private visible

---

## 📞 Recursos

- [GitHub Docs - Creating a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository)
- [GitHub Docs - Adding an existing project](https://docs.github.com/en/get-started/importing-your-projects-to-github/importing-source-code-to-github/adding-locally-hosted-code-to-github)
- [Git Documentation](https://git-scm.com/doc)

---

**¡Listo! Tu proyecto Shadow-Scan está ahora de forma segura en GitHub como repositorio privado.** 🎉
