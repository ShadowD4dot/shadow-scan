#!/bin/bash
#
# Shadow-Scan - Script de Instalación
# Instala todas las herramientas necesarias
#

set -e

echo "=================================="
echo "🕵️  Shadow-Scan - Instalación"
echo "=================================="
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar que Go está instalado
if ! command -v go &> /dev/null; then
    echo -e "${RED}❌ Go no está instalado${NC}"
    echo ""
    echo "Por favor instala Go desde: https://golang.org/dl/"
    echo ""
    echo "En Ubuntu/Debian:"
    echo "  wget https://go.dev/dl/go1.21.0.linux-amd64.tar.gz"
    echo "  sudo tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz"
    echo "  echo 'export PATH=\$PATH:/usr/local/go/bin:\$HOME/go/bin' >> ~/.bashrc"
    echo "  source ~/.bashrc"
    exit 1
fi

echo -e "${GREEN}✅ Go detectado: $(go version)${NC}"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 no está instalado${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python detectado: $(python3 --version)${NC}"
echo ""

# Instalar dependencias Python
echo -e "${YELLOW}📦 Instalando dependencias Python...${NC}"
pip3 install -r requirements.txt

echo ""
echo -e "${YELLOW}🔧 Instalando herramientas de ProjectDiscovery...${NC}"
echo ""

# Subfinder
echo "  📡 Instalando Subfinder..."
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# Httpx
echo "  🌐 Instalando Httpx..."
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

# Nuclei
echo "  🎯 Instalando Nuclei..."
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

# Actualizar templates de Nuclei
echo ""
echo -e "${YELLOW}📥 Actualizando templates de Nuclei...${NC}"
nuclei -update-templates

echo ""
echo -e "${GREEN}✅ Instalación completada${NC}"
echo ""
echo "=================================="
echo "🎯 Herramientas Instaladas:"
echo "=================================="
subfinder -version 2>&1 | head -n 1
httpx -version 2>&1 | head -n 1
nuclei -version 2>&1 | head -n 1
echo ""

echo "=================================="
echo "🚀 Siguiente Paso:"
echo "=================================="
echo ""
echo "1. Configurar Telegram (opcional):"
echo "   python3 shadow_scan_full.py --init-telegram"
echo ""
echo "2. Ejecutar un escaneo de prueba:"
echo "   python3 shadow_scan_full.py -d example.com"
echo ""
echo "3. Iniciar el dashboard:"
echo "   python3 dashboard.py"
echo ""
