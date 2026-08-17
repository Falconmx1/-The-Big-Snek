# -*- coding: utf-8 -*-

import re
import os
import sys
import socket
import subprocess
from .colors import Colors
from .logger import Logger

class Utils:
    """Clase con funciones de utilidad general."""

    def __init__(self):
        self.logger = Logger()

    # --- Validaciones ---
    def is_valid_ip(self, ip):
        """Valida si una cadena es una dirección IPv4 válida."""
        pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if not re.match(pattern, ip):
            return False
        # Verificar que cada octeto esté en el rango 0-255
        for octet in ip.split('.'):
            if not 0 <= int(octet) <= 255:
                return False
        return True

    def is_valid_port(self, port):
        """Valida si un puerto es válido (1-65535)."""
        try:
            port = int(port)
            return 1 <= port <= 65535
        except ValueError:
            return False

    def is_valid_file(self, filepath):
        """Verifica si un archivo existe y es legible."""
        return os.path.isfile(filepath) and os.access(filepath, os.R_OK)

    # --- Manejo de Archivos ---
    def read_file_lines(self, filepath):
        """
        Lee un archivo y retorna una lista de líneas (sin saltos de línea).
        Retorna None si hay error.
        """
        if not self.is_valid_file(filepath):
            self.logger.error(f"Archivo no válido o inaccesible: {filepath}")
            return None

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return [line.strip() for line in f if line.strip()]
        except Exception as e:
            self.logger.error(f"Error leyendo archivo {filepath}: {e}")
            return None

    def write_to_file(self, filepath, content, mode='w'):
        """Escribe contenido a un archivo."""
        try:
            with open(filepath, mode, encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            self.logger.error(f"Error escribiendo archivo {filepath}: {e}")
            return False

    def human_readable_size(self, size_bytes):
        """Convierte bytes a formato legible (KB, MB, GB)."""
        if size_bytes == 0:
            return "0B"
        size_names = ("B", "KB", "MB", "GB", "TB")
        i = 0
        size = float(size_bytes)
        while size >= 1024.0 and i < len(size_names) - 1:
            size /= 1024.0
            i += 1
        return f"{size:.1f} {size_names[i]}"

    # --- Sistema y Red ---
    def get_local_ip(self):
        """Obtiene la dirección IP local."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    def ping_host(self, host):
        """Realiza un ping simple a un host (verifica conectividad)."""
        param = '-n' if sys.platform.lower() == 'win32' else '-c'
        command = ['ping', param, '1', host]
        try:
            subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=2)
            return True
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            return False
        except Exception:
            return False

    def check_root(self):
        """Verifica si el script se está ejecutando como root/administrador."""
        if sys.platform.lower() == 'win32':
            try:
                # En Windows, verificar si el proceso tiene privilegios de administrador
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            except Exception:
                return False
        else:
            return os.geteuid() == 0

    # --- Misceláneos ---
    def progress_bar(self, current, total, bar_length=50):
        """Genera una barra de progreso simple."""
        progress = current / total
        arrow = '█' * int(round(progress * bar_length))
        spaces = ' ' * (bar_length - len(arrow))
        return f"[{arrow}{spaces}] {int(progress * 100)}%"

    def safe_execute(self, func, *args, **kwargs):
        """
        Ejecuta una función de forma segura, capturando cualquier excepción.
        Retorna un tuple (success, result/error_message).
        """
        try:
            result = func(*args, **kwargs)
            return True, result
        except Exception as e:
            return False, str(e)
