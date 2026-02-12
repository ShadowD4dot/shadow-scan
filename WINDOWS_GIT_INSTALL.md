# 🪟 Instalar Git en Windows

## 📥 Método 1: Instalación Estándar (Recomendado)

### Paso 1: Descargar Git

1. Ve a: https://git-scm.com/download/win
2. La descarga debería comenzar automáticamente
3. Si no, haz clic en **"Click here to download manually"**
4. Descarga el instalador de **64-bit** (probablemente `Git-2.43.0-64-bit.exe`)

### Paso 2: Instalar Git

1. Ejecuta el instalador descargado
2. En la pantalla de instalación:
   - ✅ **Select Components**: Deja todo por defecto
   - ✅ **Choosing the default editor**: Selecciona tu editor favorito (Notepad++, VS Code, etc.)
   - ✅ **Adjusting your PATH**: Selecciona **"Git from the command line and also from 3rd-party software"**
   - ✅ **Choosing HTTPS transport backend**: Deja **"Use the OpenSSL library"**
   - ✅ **Configuring the line ending conversions**: Selecciona **"Checkout Windows-style, commit Unix-style"**
   - ✅ **Configuring the terminal emulator**: Selecciona **"Use MinTTY"**
   - ✅ Resto: Deja las opciones por defecto
3. Click **Install**
4. Click **Finish**

### Paso 3: Verificar Instalación

Abre una **NUEVA ventana de PowerShell** (importante: nueva ventana) y ejecuta:

```powershell
git --version
```

Deberías ver algo como:
```
git version 2.43.0.windows.1
```

---

## 📥 Método 2: Usando Winget (Windows Package Manager)

Si tienes Windows 10/11 actualizado:

```powershell
# Abrir PowerShell como Administrador
winget install --id Git.Git -e --source winget
```

Luego **cierra y abre una nueva PowerShell** para que tome efecto.

---

## 📥 Método 3: Usando Chocolatey

Si tienes Chocolatey instalado:

```powershell
# Como Administrador
choco install git -y
```

---

## 🔧 Configuración Inicial de Git

Después de instalar, configura tu identidad:

```powershell
# Tu nombre (aparecerá en los commits)
git config --global user.name "Tu Nombre"

# Tu email
git config --global user.email "tu@email.com"

# Verificar configuración
git config --list
```

---

## 🚀 Ahora Sí: Subir a GitHub

### Opción A: Usando PowerShell con Git

```powershell
# 1. Navegar a tu proyecto
cd C:\ruta\a\shadow-scan

# 2. Crear .gitignore
@"
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
"@ | Out-File -FilePath .gitignore -Encoding UTF8

# 3. Inicializar repositorio
git init

# 4. Agregar archivos
git add .

# 5. Primer commit
git commit -m "Initial commit: Shadow-Scan"

# 6. Conectar con GitHub (reemplaza TU_USUARIO y NOMBRE_REPO)
git remote add origin https://github.com/TU_USUARIO/NOMBRE_REPO.git

# 7. Subir
git branch -M main
git push -u origin main
```

### Opción B: Usando GitHub Desktop (Más Fácil para Windows)

1. **Descargar GitHub Desktop**:
   - https://desktop.github.com/
   - Instalar y abrir

2. **Autenticarse**:
   - File → Options → Accounts → Sign in

3. **Agregar tu proyecto**:
   - File → Add local repository
   - Navegar a la carpeta `shadow-scan`
   - Si dice "no git repository", click "create a repository"

4. **Crear .gitignore**:
   - Crear archivo `.gitignore` con este contenido:
   ```
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
   ```

5. **Commit inicial**:
   - Verás todos los archivos en la izquierda
   - Abajo escribe: "Initial commit: Shadow-Scan"
   - Click "Commit to main"

6. **Publicar a GitHub**:
   - Click "Publish repository"
   - ✅ Marca **"Keep this code private"**
   - Click "Publish repository"

¡Listo! 🎉

---

## 🔑 Autenticación en GitHub

La primera vez que hagas `git push`, te pedirá credenciales:

### Método 1: Personal Access Token (Recomendado)

1. Ve a GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Scopes: Marca **`repo`** (Full control of private repositories)
4. Generate token
5. **Copia el token** (solo se muestra una vez)

Cuando Git pida password:
- **Username**: Tu usuario de GitHub
- **Password**: Pega el token (no tu contraseña normal)

### Método 2: Git Credential Manager (Automático)

Git para Windows incluye Git Credential Manager que gestiona la autenticación automáticamente. La primera vez:

1. Git te abrirá una ventana de navegador
2. Inicia sesión en GitHub
3. Autoriza el acceso
4. ¡Listo! No volverá a pedir credenciales

---

## 🛠️ Herramientas Recomendadas para Windows

### Git GUI Clients (Alternativas a línea de comandos)

1. **GitHub Desktop** (Más fácil)
   - https://desktop.github.com/
   - Interfaz visual simple

2. **GitKraken** (Potente)
   - https://www.gitkraken.com/
   - Para usuarios avanzados

3. **SourceTree** (Completo)
   - https://www.sourcetreeapp.com/
   - De Atlassian (creadores de Bitbucket)

### Editores de Código con Git Integrado

1. **VS Code** (Recomendado)
   - https://code.visualstudio.com/
   - Git integrado + extensiones

2. **PyCharm Community**
   - https://www.jetbrains.com/pycharm/
   - Perfecto para Python

---

## 📝 Script PowerShell para Setup Automático

Guarda esto como `setup-git-windows.ps1`:

```powershell
# Script de setup para Git en Windows

Write-Host "🔍 Verificando Git..." -ForegroundColor Yellow

if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Host "✅ Git está instalado: $(git --version)" -ForegroundColor Green
} else {
    Write-Host "❌ Git NO está instalado" -ForegroundColor Red
    Write-Host ""
    Write-Host "Por favor instala Git desde: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "Luego cierra y abre una nueva PowerShell" -ForegroundColor Yellow
    exit 1
}

# Solicitar información
Write-Host ""
Write-Host "📝 Configuración de Git" -ForegroundColor Cyan
$gitName = Read-Host "Tu nombre para Git"
$gitEmail = Read-Host "Tu email para Git"
$githubUser = Read-Host "Tu usuario de GitHub"
$repoName = Read-Host "Nombre del repositorio (default: shadow-scan)"
if ([string]::IsNullOrWhiteSpace($repoName)) { $repoName = "shadow-scan" }

# Configurar Git
Write-Host ""
Write-Host "🔧 Configurando Git..." -ForegroundColor Yellow
git config --global user.name "$gitName"
git config --global user.email "$gitEmail"
Write-Host "✅ Git configurado" -ForegroundColor Green

# Crear .gitignore
Write-Host ""
Write-Host "📝 Creando .gitignore..." -ForegroundColor Yellow
@"
__pycache__/
*.py[cod]
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
"@ | Out-File -FilePath .gitignore -Encoding UTF8
Write-Host "✅ .gitignore creado" -ForegroundColor Green

# Inicializar Git
Write-Host ""
Write-Host "📦 Inicializando repositorio..." -ForegroundColor Yellow
git init
git add .
git commit -m "Initial commit: Shadow-Scan - Automated Attack Surface Scanner"
Write-Host "✅ Repositorio inicializado" -ForegroundColor Green

# Instrucciones finales
Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "✅ Repositorio Git Preparado" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Siguientes pasos:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Crear repositorio PRIVADO en GitHub:"
Write-Host "   https://github.com/new"
Write-Host ""
Write-Host "   - Repository name: $repoName"
Write-Host "   - Visibility: 🔒 Private"
Write-Host "   - NO marques 'Add README'"
Write-Host ""
Write-Host "2. Ejecuta estos comandos:" -ForegroundColor Cyan
Write-Host ""
Write-Host "git remote add origin https://github.com/$githubUser/$repoName.git" -ForegroundColor White
Write-Host "git branch -M main" -ForegroundColor White
Write-Host "git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  Cuando pida password, usa tu Personal Access Token" -ForegroundColor Yellow
Write-Host "   (No tu contraseña normal de GitHub)" -ForegroundColor Yellow
Write-Host ""
Write-Host "🎉 ¡Listo para subir a GitHub!" -ForegroundColor Green
```

Ejecutar:
```powershell
.\setup-git-windows.ps1
```

---

## 🆘 Problemas Comunes en Windows

### "git no reconocido" después de instalar

**Solución**: Cierra **TODAS** las ventanas de PowerShell y abre una nueva

### "Permission denied" al hacer push

**Solución**: 
1. Usar Personal Access Token en lugar de password
2. O configurar SSH key (más complejo en Windows)

### "LF will be replaced by CRLF"

**Solución**: Es solo una advertencia, puedes ignorarla. Git está convirtiendo finales de línea automáticamente.

### Caracteres raros en los archivos

**Solución**: Configurar encoding UTF-8:
```powershell
git config --global core.autocrlf true
```

---

## ✅ Checklist Post-Instalación

- [ ] Git instalado
- [ ] `git --version` funciona
- [ ] Git configurado (name y email)
- [ ] .gitignore creado
- [ ] Repositorio inicializado
- [ ] Commit inicial hecho
- [ ] Repositorio en GitHub creado (PRIVATE)
- [ ] Push exitoso

---

## 📞 Recursos

- [Git para Windows](https://git-scm.com/download/win)
- [GitHub Desktop](https://desktop.github.com/)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Docs](https://docs.github.com/)

---

**¡Una vez instalado Git, vuelve a ejecutar los comandos de setup!** 🚀
