# -*- coding: utf-8 -*-

import sys
import time
from .colors import Colors

class Logger:
    """Clase para gestionar logs con niveles y colores."""

    # Niveles de log
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4
    SILENT = 5

    def __init__(self, level=INFO, use_colors=True):
        """
        Inicializa el logger.
        :param level: Nivel mínimo de log a mostrar.
        :param use_colors: Si se deben usar colores en la salida.
        """
        self.level = level
        self.use_colors = use_colors
        self.log_file = None

    def set_level(self, level):
        """Cambia el nivel de log actual."""
        self.level = level

    def set_log_file(self, filepath):
        """Configura un archivo para guardar los logs."""
        try:
            self.log_file = open(filepath, 'a')
        except Exception as e:
            self.error(f"No se pudo abrir el archivo de log: {e}")

    def _log(self, message, level, level_name, color):
        """Método interno para formatear y mostrar un mensaje."""
        if level < self.level:
            return

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] [{level_name}] {message}"

        # Salida a consola
        if self.use_colors:
            print(f"{color}{log_line}{Colors.RESET}")
        else:
            print(log_line)

        # Salida a archivo
        if self.log_file:
            try:
                self.log_file.write(log_line + '\n')
                self.log_file.flush()
            except Exception as e:
                # No usar el logger aquí para evitar recursión
                print(f"[!] Error escribiendo en archivo de log: {e}")

    def debug(self, message):
        self._log(message, self.DEBUG, "DEBUG", Colors.CYAN)

    def info(self, message):
        self._log(message, self.INFO, "INFO", Colors.GREEN)

    def warning(self, message):
        self._log(message, self.WARNING, "WARNING", Colors.YELLOW)

    def error(self, message):
        self._log(message, self.ERROR, "ERROR", Colors.RED)

    def critical(self, message):
        self._log(message, self.CRITICAL, "CRITICAL", Colors.BOLD_RED)

    def raw(self, message):
        """Imprime un mensaje sin formato (sin timestamp ni nivel)."""
        if self.use_colors:
            print(message)
        else:
            # Eliminar códigos de color para salida sin colores
            import re
            clean_message = re.sub(r'\033\[[0-9;]*m', '', message)
            print(clean_message)

    def close(self):
        """Cierra el archivo de log si está abierto."""
        if self.log_file:
            self.log_file.close()
            self.log_file = None
