#!/bin/bash
# install.sh - Instalador de The Big Snek

set -e

# Colores para la terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}"
echo "╔════════════════════════════════════════════╗"
echo "║     🐍 The Big Snek - Instalador         ║"
echo "║   Ligero, rápido y que no deja huella    ║"
echo "╚════════════════════════════════════════════╝"
echo -e "${NC}"

# Verificar Python
echo -e "${BLUE}[*] Verificando Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2)
    echo -e "${GREEN}[+] Python $PYTHON_VERSION encontrado${NC}"
else
    echo -e "${RED}[!] Error: Python 3 no está instalado.${NC}"
    echo -e "${YELLOW}[*] Instala Python 3 y vuelve a intentarlo.${NC}"
    exit 1
fi

# Crear estructura de directorios
echo -e "${BLUE}[*] Creando estructura de directorios...${NC}"
mkdir -p modules core wordlists templates backdoors logs

# Verificar permisos de ejecución
echo -e "${BLUE}[*] Estableciendo permisos...${NC}"
chmod +x snek.py 2>/dev/null || echo -e "${YELLOW}[!] snek.py no encontrado, saltando...${NC}"

# Instalar dependencias básicas
echo -e "${BLUE}[*] Instalando dependencias básicas...${NC}"
echo -e "${YELLOW}[?] ¿Deseas instalar dependencias adicionales? (y/N)${NC}"
read -r INSTALL_DEPS

if [[ "$INSTALL_DEPS" =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}[*] Instalando dependencias...${NC}"
    
    # Pillow para manejo de imágenes
    echo -e "${YELLOW}[*] Instalando Pillow...${NC}"
    pip3 install pillow 2>/dev/null || pip install pillow 2>/dev/null || echo -e "${YELLOW}[!] No se pudo instalar Pillow${NC}"
    
    # Otras dependencias opcionales
    echo -e "${YELLOW}[*] Instalando requests...${NC}"
    pip3 install requests 2>/dev/null || pip install requests 2>/dev/null || echo -e "${YELLOW}[!] No se pudo instalar requests${NC}"
    
    echo -e "${GREEN}[+] Dependencias instaladas${NC}"
fi

# Crear wordlist por defecto
echo -e "${BLUE}[*] Creando wordlist por defecto...${NC}"
if [ ! -f "wordlists/top1000.txt" ]; then
    cat > wordlists/top1000.txt << 'EOF'
123456
password
12345678
qwerty
123456789
12345
1234
111111
1234567
dragon
123123
baseball
abc123
football
monkey
letmein
shadow
master
666666
qwertyuiop
123321
mustang
1234567890
michael
654321
superman
1qaz2wsx
7777777
121212
000000
qazwsx
123qwe
killer
trustno1
jordan
jennifer
zxcvbnm
asdfgh
hunter
buster
soccer
batman
fuckyou
harley
hello
chelsea
lovely
fuckme
orange
pepper
phoenix
tigger
computer
amanda
hannah
thunder
knight
ginger
hardcore
sweet
princess
joshua
tigger
butterfly
matrix
maggie
freedom
fuckoff
abigail
pussy
cowboy
madison
pokemon
maverick
spiderman
mustang
richard
coffee
qwerty123
fuck
awesome
jasmine
welcome
cameron
secret
whocares
dallas
mickey
rocky
hello123
qwerty1
newyork
test
nick
mexico
snoopy
peanut
dark
pookie
alex
brandy
prince
marina
patrick
summer
jackie
anthony
cookie
ninja
jacob
panther
pepper
EOF
    echo -e "${GREEN}[+] Wordlist creada en wordlists/top1000.txt${NC}"
else
    echo -e "${YELLOW}[!] Wordlist ya existe${NC}"
fi

# Crear archivo de logs
touch logs/snek.log
echo -e "${GREEN}[+] Archivo de log creado en logs/snek.log${NC}"

# Mensaje final
echo -e "\n${GREEN}╔════════════════════════════════════════════╗"
echo -e "║    ✅ Instalación completada con éxito    ║"
echo -e "╚════════════════════════════════════════════╝${NC}"

echo -e "\n${CYAN}[*] Resumen:${NC}"
echo -e "  📁 Directorios creados: core/, modules/, wordlists/, templates/, backdoors/, logs/"
echo -e "  📄 Wordlist: wordlists/top1000.txt"
echo -e "  📝 Logs: logs/snek.log"
echo -e "  🐍 Python: $PYTHON_VERSION"

echo -e "\n${YELLOW}[*] Para ejecutar The Big Snek:${NC}"
echo -e "  python3 snek.py"
echo -e "  python3 snek.py --help"
echo -e "  python3 snek.py scan -t 192.168.1.1 -p 1-1000"

echo -e "\n${CYAN}[*] Módulos disponibles:${NC}"
echo -e "  🔍 scan     - Escáner de puertos"
echo -e "  🔓 crack    - Fuerza bruta de hashes"
echo -e "  📁 dump     - Extractor de metadatos"
echo -e "  🎣 phish    - Generador de phishing"
echo -e "  🔒 persist  - Persistencia y backdoors"

echo -e "\n${GREEN}🐍 ¡The Big Snek está listo para usar!${NC}"
echo -e "${YELLOW}⚠️  Recuerda usar estas herramientas solo con autorización.${NC}\n"
