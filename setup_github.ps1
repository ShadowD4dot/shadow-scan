# Shadow-Scan - Setup Git en Windows
# PowerShell Script

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "🔒 Shadow-Scan - Setup GitHub" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que estamos en el directorio correcto
if (-Not (Test-Path "shadow_scan.py")) {
    Write-Host "❌ Error: Ejecuta este script desde el directorio shadow-scan" -ForegroundColor Red
    exit 1
}

# Verificar Git
Write-Host "🔍 Verificando Git..." -ForegroundColor Yellow
try {
    $gitVersion = git --version
    Write-Host "✅ Git detectado: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git NO está instalado" -ForegroundColor Red
    Write-Host ""
    Write-Host "📥 Descarga Git desde: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "O instala con winget:" -ForegroundColor Yellow
    Write-Host "  winget install --id Git.Git -e --source winget" -ForegroundColor White
    Write-Host ""
    Write-Host "Después de instalar, cierra y abre una NUEVA PowerShell" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Presiona Enter para abrir la página de descarga"
    Start-Process "https://git-scm.com/download/win"
    exit 1
}

Write-Host ""

# Solicitar información del usuario
Write-Host "📝 Configuración de Git" -ForegroundColor Cyan
Write-Host ""

$gitName = Read-Host "Tu nombre para Git"
$gitEmail = Read-Host "Tu email para Git"
$githubUser = Read-Host "Tu usuario de GitHub"
$repoName = Read-Host "Nombre del repositorio (presiona Enter para 'shadow-scan')"

if ([string]::IsNullOrWhiteSpace($repoName)) {
    $repoName = "shadow-scan"
}

Write-Host ""
Write-Host "📋 Configuración:" -ForegroundColor Blue
Write-Host "  Nombre: $gitName"
Write-Host "  Email: $gitEmail"
Write-Host "  Usuario GitHub: $githubUser"
Write-Host "  Repositorio: $repoName"
Write-Host ""

$confirm = Read-Host "¿Es correcto? (s/n)"
if ($confirm -ne "s") {
    Write-Host "Cancelado" -ForegroundColor Yellow
    exit 0
}

# Configurar Git
Write-Host ""
Write-Host "🔧 Configurando Git..." -ForegroundColor Yellow
git config --global user.name "$gitName"
git config --global user.email "$gitEmail"
Write-Host "✅ Git configurado" -ForegroundColor Green

# Crear .gitignore
Write-Host ""
Write-Host "📝 Creando .gitignore..." -ForegroundColor Yellow

$gitignoreContent = @"
# Python
__pycache__/
*.py[cod]
*`$py.class
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

# Configuración sensible (IMPORTANTE - NO SUBIR)
.telegram_config.json
.env
*.key
*.pem
targets.txt

# Archivos temporales
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
"@

$gitignoreContent | Out-File -FilePath .gitignore -Encoding UTF8
Write-Host "✅ .gitignore creado" -ForegroundColor Green

# Verificar archivos sensibles
Write-Host ""
Write-Host "🔍 Verificando archivos sensibles..." -ForegroundColor Yellow

$sensitiveFiles = @(".telegram_config.json", ".env", "targets.txt", "scans.db")
$foundSensitive = $false

foreach ($file in $sensitiveFiles) {
    if (Test-Path $file) {
        Write-Host "⚠️  Encontrado: $file (será ignorado por git)" -ForegroundColor Yellow
        $foundSensitive = $true
    }
}

if (-not $foundSensitive) {
    Write-Host "✅ No se encontraron archivos sensibles" -ForegroundColor Green
}

# Inicializar Git
Write-Host ""
Write-Host "📦 Inicializando repositorio Git..." -ForegroundColor Yellow

if (Test-Path ".git") {
    Write-Host "⚠️  El repositorio Git ya existe" -ForegroundColor Yellow
    $reinit = Read-Host "¿Deseas reinicializarlo? (s/n)"
    if ($reinit -eq "s") {
        Remove-Item -Recurse -Force .git
        git init
        Write-Host "✅ Repositorio reinicializado" -ForegroundColor Green
    }
} else {
    git init
    Write-Host "✅ Repositorio inicializado" -ForegroundColor Green
}

# Agregar archivos
Write-Host ""
Write-Host "📁 Agregando archivos..." -ForegroundColor Yellow
git add .
Write-Host "✅ Archivos agregados" -ForegroundColor Green

# Mostrar estado
Write-Host ""
Write-Host "📊 Estado del repositorio:" -ForegroundColor Yellow
git status --short

# Crear commit inicial
Write-Host ""
Write-Host "💾 Creando commit inicial..." -ForegroundColor Yellow

$commitMessage = @"
Initial commit: Shadow-Scan - Automated Attack Surface Scanner

Features:
- Subfinder + Httpx + Nuclei integration
- Telegram notifications
- Interactive web dashboard
- Automated scanning with cron
- Demo mode for testing
"@

git commit -m $commitMessage
Write-Host "✅ Commit creado" -ForegroundColor Green

# Instrucciones finales
Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "✅ Repositorio Git Preparado" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Siguientes pasos:" -ForegroundColor Blue
Write-Host ""
Write-Host "1️⃣  Crear repositorio PRIVADO en GitHub:" -ForegroundColor Yellow
Write-Host "   https://github.com/new" -ForegroundColor White
Write-Host ""
Write-Host "   Configuración:"
Write-Host "   - Repository name: $repoName"
Write-Host "   - Visibility: 🔒 Private"
Write-Host "   - NO marques 'Add README'"
Write-Host ""
Write-Host "2️⃣  Conectar con GitHub:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   Copia y ejecuta estos comandos:" -ForegroundColor Cyan
Write-Host ""
Write-Host "   git remote add origin https://github.com/$githubUser/$repoName.git" -ForegroundColor White
Write-Host "   git branch -M main" -ForegroundColor White
Write-Host "   git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "3️⃣  Autenticación:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   Cuando te pida credenciales:" -ForegroundColor Cyan
Write-Host "   - Username: $githubUser"
Write-Host "   - Password: Tu Personal Access Token (NO tu contraseña)" -ForegroundColor Yellow
Write-Host ""
Write-Host "   Para crear un token:" -ForegroundColor Cyan
Write-Host "   GitHub → Settings → Developer settings → Personal access tokens"
Write-Host "   → Generate new token (classic) → Scope: 'repo'" -ForegroundColor Gray
Write-Host ""
Write-Host "4️⃣  Verificar que es privado:" -ForegroundColor Yellow
Write-Host "   https://github.com/$githubUser/$repoName" -ForegroundColor White
Write-Host "   Debe tener badge 🔒 Private"
Write-Host ""
Write-Host "⚠️  IMPORTANTE:" -ForegroundColor Red
Write-Host "   Verifica que .telegram_config.json NO esté en el repositorio"
Write-Host "   Verifica que scan_results/ NO esté en el repositorio"
Write-Host ""
Write-Host "🎉 ¡Listo para subir a GitHub!" -ForegroundColor Green
Write-Host ""

# Guardar comandos en archivo
$commandsContent = @"
# Comandos para conectar con GitHub
# Ejecuta estos comandos después de crear el repositorio en GitHub

# Conectar repositorio
git remote add origin https://github.com/$githubUser/$repoName.git
git branch -M main
git push -u origin main

# Verificar
git remote -v

# Crear Personal Access Token:
# https://github.com/settings/tokens/new
# Scope: repo (Full control of private repositories)
"@

$commandsContent | Out-File -FilePath github_commands.txt -Encoding UTF8

Write-Host "💡 Los comandos también se guardaron en: github_commands.txt" -ForegroundColor Blue
Write-Host ""
Write-Host "📖 Para más ayuda, consulta:" -ForegroundColor Cyan
Write-Host "   - WINDOWS_GIT_INSTALL.md (instalación de Git)"
Write-Host "   - GITHUB_GUIDE.md (guía completa)"
Write-Host "   - QUICK_GITHUB.md (guía rápida)"
Write-Host ""

# Preguntar si abrir GitHub
$openGithub = Read-Host "¿Abrir GitHub para crear el repositorio? (s/n)"
if ($openGithub -eq "s") {
    Start-Process "https://github.com/new"
}

Write-Host ""
Write-Host "✨ Setup completado exitosamente" -ForegroundColor Green
Write-Host ""
