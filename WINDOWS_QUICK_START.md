# 🪟 Guía Rápida para Windows

## ⚡ Opción 1: GitHub Desktop (MÁS FÁCIL - RECOMENDADO)

### 1. Instalar GitHub Desktop
- Descarga: https://desktop.github.com/
- Instala y abre la aplicación
- File → Options → Accounts → Sign in to GitHub.com

### 2. Crear .gitignore
Crea un archivo llamado `.gitignore` en la carpeta shadow-scan con este contenido:

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
.vscode/
.DS_Store
```

**💡 Cómo crear .gitignore en Windows:**
```powershell
# En PowerShell, dentro de la carpeta shadow-scan:
notepad .gitignore
# Pega el contenido de arriba → Guardar
```

### 3. Agregar tu proyecto a GitHub Desktop
- File → Add local repository
- Navega a tu carpeta `shadow-scan`
- Si dice "This directory does not appear to be a Git repository":
  - Click "create a repository here instead"

### 4. Hacer commit inicial
- Verás todos los archivos en el panel izquierdo
- En la esquina inferior izquierda escribe: "Initial commit: Shadow-Scan"
- Click botón azul **"Commit to main"**

### 5. Publicar a GitHub
- Click botón azul **"Publish repository"**
- ✅ **MUY IMPORTANTE**: Marca la casilla **"Keep this code private"**
- Click **"Publish repository"**

### ✅ ¡Listo! Tu proyecto está en GitHub de forma privada 🎉

Para ver tu repositorio: https://github.com/TU_USUARIO/shadow-scan

---

## ⚡ Opción 2: Línea de Comandos (PowerShell)

### Paso 1: Instalar Git

**Opción A - Instalador manual:**
1. Descarga: https://git-scm.com/download/win
2. Instala (siguiente → siguiente → instalar)
3. **CIERRA Y ABRE NUEVA PowerShell**

**Opción B - Con Winget:**
```powershell
# Como Administrador
winget install --id Git.Git -e --source winget
```

### Paso 2: Ejecutar script automático

```powershell
# Navega a tu carpeta
cd C:\ruta\a\shadow-scan

# Ejecuta el script
.\setup_github.ps1

# Si da error de "no se puede ejecutar scripts":
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup_github.ps1
```

### Paso 3: Crear repositorio en GitHub

1. Abre: https://github.com/new
2. **Repository name**: shadow-scan
3. **Visibility**: 🔒 Private
4. ❌ NO marques nada más
5. Click **"Create repository"**

### Paso 4: Ejecutar comandos

Copia y ejecuta los comandos que te mostró el script:

```powershell
git remote add origin https://github.com/TU_USUARIO/shadow-scan.git
git branch -M main
git push -u origin main
```

Cuando pida credenciales:
- **Username**: Tu usuario de GitHub
- **Password**: Tu **Personal Access Token** (NO tu contraseña)

---

## 🔑 Crear Personal Access Token

1. GitHub → Click tu foto (arriba derecha) → Settings
2. Developer settings (abajo a la izquierda)
3. Personal access tokens → Tokens (classic)
4. Generate new token (classic)
5. **Note**: "Shadow-Scan Windows"
6. **Expiration**: 90 days (o lo que prefieras)
7. **Scopes**: ✅ Marca solo `repo` (Full control of private repositories)
8. Click **"Generate token"**
9. **COPIA EL TOKEN** (solo se muestra una vez) → Guárdalo en un lugar seguro

---

## 🆘 Solución de Problemas

### "git no reconocido como comando"

**Causa**: Git no está instalado o PowerShell no se reinició

**Solución**:
1. Cierra TODAS las ventanas de PowerShell
2. Abre una NUEVA PowerShell
3. Escribe: `git --version`
4. Si aún no funciona, reinstala Git

---

### "No se pueden ejecutar scripts en este sistema"

**Causa**: Política de ejecución de PowerShell

**Solución**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### "Permission denied al hacer push"

**Causa**: Credenciales incorrectas

**Solución**:
- Usa tu **Personal Access Token** como password (NO tu contraseña de GitHub)
- Crea uno nuevo si lo perdiste

---

### "El archivo .gitignore no se crea"

**Solución con Notepad**:
```powershell
notepad .gitignore
# Pega el contenido → Guardar
```

**Solución con PowerShell**:
```powershell
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
"@ | Out-File -FilePath .gitignore -Encoding UTF8
```

---

## 📊 Comparación de Métodos

| Método | Dificultad | Tiempo | Recomendado para |
|--------|------------|--------|------------------|
| **GitHub Desktop** | ⭐ Fácil | 5 min | Principiantes |
| **Script PowerShell** | ⭐⭐ Medio | 10 min | Usuarios intermedios |
| **Manual con Git** | ⭐⭐⭐ Avanzado | 15 min | Expertos |

---

## ✅ Verificación Final

Después de subir, verifica:

- [ ] El repositorio aparece en: https://github.com/TU_USUARIO/shadow-scan
- [ ] Tiene el badge **🔒 Private**
- [ ] Todos los archivos están ahí
- [ ] **NO** aparece `.telegram_config.json`
- [ ] **NO** aparece la carpeta `scan_results/`

---

## 🔄 Futuras Actualizaciones

### Con GitHub Desktop:
1. Haz cambios en los archivos
2. Aparecerán en el panel izquierdo
3. Escribe mensaje de commit
4. Click "Commit to main"
5. Click "Push origin"

### Con PowerShell:
```powershell
git add .
git commit -m "Descripción del cambio"
git push
```

---

## 📚 Recursos para Windows

- **Git para Windows**: https://git-scm.com/download/win
- **GitHub Desktop**: https://desktop.github.com/
- **VS Code** (editor recomendado): https://code.visualstudio.com/
- **Windows Terminal** (mejor que PowerShell): https://aka.ms/terminal

---

## 💡 Recomendación Final

**Para Windows, te recomiendo usar GitHub Desktop** porque:
- ✅ No requiere línea de comandos
- ✅ Interfaz visual clara
- ✅ Manejo automático de credenciales
- ✅ Menos probabilidad de errores
- ✅ Ideal para principiantes

**Solo necesitas:**
1. Crear el archivo `.gitignore`
2. Instalar GitHub Desktop
3. Agregar proyecto
4. Commit
5. Publish (marcando "Private")

**¡En menos de 5 minutos está listo!** 🚀
