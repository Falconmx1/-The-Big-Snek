#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The Big Snek - El cuchillo suizo del pentester moderno.
Uso: python snek.py [modulo] [opciones]
"""

import sys
import os
import argparse
from core.colors import Colors
from core.logger import Logger
from core.utils import Utils

class BigSnek:
    """Clase principal que gestiona la ejecución de módulos."""

    def __init__(self):
        self.logger = Logger()
        self.utils = Utils()
        self.modules_path = os.path.join(os.path.dirname(__file__), 'modules')

    def show_banner(self):
        """Muestra el banner de inicio."""
        banner = f"""
{Colors.GREEN}
  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄ 
 ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
 ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ 
 ▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌          
 ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄▄▄ 
 ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌
  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀ 
{Colors.RESET}
{Colors.YELLOW}🐍 The Big Snek - "Ligero, rápido y que no deja huella"{Colors.RESET}
        """
        print(banner)

    def list_modules(self):
        """Lista los módulos disponibles en el directorio 'modules/'."""
        if not os.path.exists(self.modules_path):
            self.logger.error("Directorio 'modules/' no encontrado.")
            return []

        modules = []
        for file in os.listdir(self.modules_path):
            if file.endswith('.py') and not file.startswith('__'):
                modules.append(file.replace('.py', ''))
        return modules

    def run_module(self, module_name, args):
        """Ejecuta un módulo específico importándolo dinámicamente."""
        module_file = os.path.join(self.modules_path, f"{module_name}.py")
        if not os.path.exists(module_file):
            self.logger.error(f"Módulo '{module_name}' no encontrado.")
            return False

        try:
            # Importación dinámica del módulo
            import importlib.util
            spec = importlib.util.spec_from_file_location(module_name, module_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Verificar si tiene una función main
            if hasattr(module, 'main'):
                module.main(args)
                return True
            else:
                self.logger.error(f"El módulo '{module_name}' no tiene una función 'main'.")
                return False
        except Exception as e:
            self.logger.error(f"Error al ejecutar el módulo '{module_name}': {e}")
            return False

    def main(self):
        """Función principal que procesa argumentos y ejecuta el flujo."""
        self.show_banner()

        parser = argparse.ArgumentParser(description="The Big Snek - Framework de seguridad modular.")
        parser.add_argument('module', nargs='?', help="Nombre del módulo a ejecutar.")
        parser.add_argument('args', nargs=argparse.REMAINDER, help="Argumentos para el módulo.")

        # Si no hay argumentos, mostrar ayuda y módulos disponibles
        if len(sys.argv) == 1:
            modules = self.list_modules()
            print(f"{Colors.CYAN}Módulos disponibles:{Colors.RESET}")
            for mod in modules:
                print(f"  - {mod}")
            print(f"\n{Colors.YELLOW}Uso: python snek.py [modulo] [argumentos...]{Colors.RESET}")
            return

        args = parser.parse_args()

        if args.module:
            # Pasar los argumentos restantes al módulo
            self.run_module(args.module, args.args)
        else:
            parser.print_help()

if __name__ == "__main__":
    try:
        snek = BigSnek()
        snek.main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Interrupción detectada. Saliendo...{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}[!] Error crítico: {e}{Colors.RESET}")
        sys.exit(1)
