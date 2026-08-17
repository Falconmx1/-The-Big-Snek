🐍 The Big Snek
"Ligero, rápido y que no deja huella"

https://img.shields.io/badge/License-MIT-blue.svg
https://img.shields.io/badge/python-3.6+-blue.svg
https://img.shields.io/badge/platform-Linux%2520%257C%2520Windows%2520%257C%2520macOS-lightgrey.svg

El cuchillo suizo del pentester moderno. Un framework modular de línea de comandos que corre en cualquier lado sin dejar rastro.

📖 Tabla de Contenidos
Características

Módulos Disponibles

Instalación Rápida

Uso Básico

Estructura del Proyecto

Ejemplos de Uso

Requisitos

Contribuciones

Licencia

Aviso Legal

✨ Características
🔌 Modular: Cada herramienta es independiente y ejecutable por sí sola

💨 Ligero: Sin dependencias pesadas, corre con Python puro

🕵️ Sin huellas: No instala dependencias globales ni deja archivos de configuración

🎯 Multiplataforma: Funciona en Linux, Windows y macOS

⚡ Rápido: Optimizado para rendimiento sin sacrificar funcionalidad

🛡️ Seguro: Diseñado para entornos controlados y pruebas autorizadas

🛠️ Módulos Disponibles
Módulo                Función                                                                  ¿Por qué no usar otra herramienta?
snek-scan             Escaneo rápido de puertos y servicios                                    Escáner SYN propio sin privilegios
snek-crack            Fuerza bruta de hashes (WPA2, MD5, SHA1)                                 Motor de crackeo optimizado para CPU
snek-dump             Extrae metadatos de archivos (PDFs, imágenes, documentos)                Parser interno sin depender de exiftool             
snek-phish            Genera páginas de phishing clonadas                                      Servidor HTTP embebido, sin Apache/NGINX
snek-persist          Crea puertas traseras y persistencia                                     Genera systemd services y tareas programadas

🚀 Instalación Rápida
Método 1: Clonar el repositorio

git clone https://github.com/Falconmx1/-The-Big-Snek.git
cd The-Big-Snek
chmod +x install.sh
./install.sh
Método 2: Descarga manual

# Crear estructura de directorios
mkdir -p The-Big-Snek/{core,modules,wordlists,templates,backdoors,logs}
cd The-Big-Snek

# Descargar archivos principales
wget https://raw.githubusercontent.com/Falconmx1/-The-Big-Snek/main/snek.py
wget https://raw.githubusercontent.com/Falconmx1/-The-Big-Snek/main/install.sh
chmod +x install.sh
./install.sh
📖 Uso Básico
Modo Navaja (Framework completo)

# Mostrar ayuda y módulos disponibles
./snek.py

# Ejecutar un módulo específico
./snek.py [modulo] [argumentos]
Módulos Individuales

# Escaneo de puertos
./modules/scan.py -t 192.168.1.1 -p 1-1000

# Crackeo de hashes
./modules/crack.py -h hashes.txt -w wordlists/top1000.txt

# Extracción de metadatos
./modules/dump.py -f documento.pdf

# Servidor de phishing
./modules/phish.py -s facebook -p 8080

# Persistencia
./modules/persist.py -m systemd -c "python3 /path/to/backdoor.py"

💡 Ejemplos de Uso
1. Escaneo de Puertos

# Escaneo básico
./snek.py scan -t 192.168.1.1 -p 1-1000

# Escaneo con más hilos y timeout personalizado
./snek.py scan -t google.com -p 1-65535 --threads 200 --timeout 0.5

# Escanear puertos específicos
./snek.py scan -t 192.168.1.1 -p 80,443,8080,3306

# Modo verboso (muestra progreso detallado)
./snek.py scan -t 192.168.1.1 -p 1-1000 -v
2. Fuerza Bruta de Hashes

# Crackear hashes MD5
./snek.py crack -h hashes.txt -w wordlists/top1000.txt

# Usar algoritmo SHA256
./snek.py crack -h hashes.txt -w wordlists/top1000.txt -a sha256

# Generar un hash de ejemplo para probar
./snek.py crack --generate "md5 password123"

# Modo verboso con más hilos
./snek.py crack -h hashes.txt -w wordlists/top1000.txt -v --threads 8
3. Extracción de Metadatos

# Extraer metadatos de una imagen
./snek.py dump -f foto.jpg

# Extraer metadatos de un PDF
./snek.py dump -f documento.pdf

# Guardar resultados en JSON
./snek.py dump -f archivo.jpg --output metadata.json

# Modo verboso
./snek.py dump -f documento.pdf -v
4. Servidor de Phishing

# Iniciar servidor de phishing para Facebook
./snek.py phish -s facebook -p 8080

# Iniciar servidor para Gmail en puerto 80 (requiere root)
sudo ./snek.py phish -s gmail -p 80

# Modo verboso
./snek.py phish -s banco -p 8080 -v

# Las credenciales capturadas se guardan en phish_logs.txt
5. Persistencia y Backdoors
6. 
# Crear servicio systemd en Linux
./snek.py persist -m systemd -c "python3 /root/backdoor.py"

# Crear tarea programada en Windows
./snek.py persist -m schtasks -c "C:\backdoor.exe"

# Agregar al inicio del sistema (multi-plataforma)
./snek.py persist -m startup -c "python3 /home/user/backdoor.py"

# Crear cron job en Linux
./snek.py persist -m cron -c "python3 /home/user/backdoor.py"

# Generar un backdoor reverse shell
./snek.py persist -m backdoor

Instalación de dependencias opcionales
# Instalar todas las dependencias opcionales
pip3 install pillow requests

# O usando el instalador interactivo
./install.sh  # y seleccionar 'y' cuando pregunte

🔒 Aviso Legal
The Big Snek está diseñado para fines educativos y de seguridad ofensiva autorizada.

⚠️ ADVERTENCIA
NO uses esta herramienta en sistemas sin autorización explícita

NO la uses para actividades ilegales o maliciosas

SIEMPRE obtén permiso por escrito antes de probar en sistemas ajenos

EL USO INDEBIDO puede ser ilegal y tener graves consecuencias

El autor no se hace responsable del mal uso de esta herramienta. Úsala bajo tu propio riesgo y responsabilidad.

Usos permitidos
✅ Pruebas de penetración autorizadas
✅ Entornos de laboratorio y educación
✅ Investigación de seguridad
✅ Auditorías de seguridad internas

Usos prohibidos
❌ Ataques a sistemas sin autorización
❌ Robo de información personal
❌ Actividades maliciosas
❌ Violación de privacidad

🌟 Agradecimientos
A la comunidad de seguridad por su constante innovación

A todos los contribuyentes que hacen posible este proyecto

A los pentesters y entusiastas de la seguridad que usan estas herramientas para aprender

📞 Contacto
GitHub: @Falconmx1

Proyecto: The Big Snek

⭐ Si te gusta "The Big Snek", ¡déjanos una estrella en GitHub! ⭐
