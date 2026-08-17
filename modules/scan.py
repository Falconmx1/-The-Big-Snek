#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de escaneo rápido de puertos y servicios.
Uso: python scan.py -t 192.168.1.1 -p 1-1000
"""

import sys
import os
import socket
import argparse
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Añadir el directorio padre al path para importar core
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.colors import Colors
from core.logger import Logger
from core.utils import Utils

class PortScanner:
    """Escáner de puertos SYN-like sin privilegios."""

    def __init__(self, target, ports, timeout=1, threads=100, verbose=False):
        self.target = target
        self.ports = ports
        self.timeout = timeout
        self.threads = threads
        self.verbose = verbose
        self.logger = Logger()
        self.utils = Utils()
        self.open_ports = []
        self.services = {}

        # Diccionario de servicios comunes
        self.service_map = {
            20: 'FTP-data', 21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
            53: 'DNS', 80: 'HTTP', 110: 'POP3', 111: 'RPC', 135: 'MSRPC',
            139: 'NetBIOS', 143: 'IMAP', 443: 'HTTPS', 445: 'SMB',
            993: 'IMAPS', 995: 'POP3S', 1723: 'PPTP', 3306: 'MySQL',
            3389: 'RDP', 5432: 'PostgreSQL', 5900: 'VNC', 6379: 'Redis',
            8080: 'HTTP-Alt', 8443: 'HTTPS-Alt', 27017: 'MongoDB'
        }

    def scan_port(self, port):
        """Intenta conectar a un puerto específico."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((self.target, port))
            sock.close()

            if result == 0:
                service = self.service_map.get(port, 'Unknown')
                self.open_ports.append(port)
                self.services[port] = service
                if self.verbose:
                    self.logger.info(f"Puerto {port} abierto - {service}")
                return port, service
        except Exception:
            pass
        return None

    def scan(self):
        """Ejecuta el escaneo con múltiples hilos."""
        print(f"\n{Colors.CYAN}[*] Escaneando {self.target}...{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Puertos: {self.ports[0]}-{self.ports[-1]} ({len(self.ports)} puertos){Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Hilos: {self.threads}{Colors.RESET}\n")

        start_time = time.time()
        scanned = 0

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            # Crear diccionario de futuros
            future_to_port = {executor.submit(self.scan_port, port): port for port in self.ports}

            for future in as_completed(future_to_port):
                port = future_to_port[future]
                scanned += 1

                # Mostrar progreso cada 100 puertos
                if scanned % 100 == 0:
                    progress = (scanned / len(self.ports)) * 100
                    print(f"{Colors.CYAN}[*] Progreso: {progress:.1f}% ({scanned}/{len(self.ports)}){Colors.RESET}", end='\r')

                try:
                    result = future.result()
                except Exception:
                    pass

        elapsed_time = time.time() - start_time
        self.print_results(elapsed_time)
        return self.open_ports, self.services

    def print_results(self, elapsed_time):
        """Muestra los resultados del escaneo."""
        print(f"\n\n{Colors.GREEN}╔════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.GREEN}║         RESULTADOS DEL ESCANEO           ║{Colors.RESET}")
        print(f"{Colors.GREEN}╚════════════════════════════════════════════╝{Colors.RESET}")

        if not self.open_ports:
            print(f"{Colors.RED}[!] No se encontraron puertos abiertos.{Colors.RESET}")
            return

        print(f"\n{Colors.CYAN}[+] {len(self.open_ports)} puertos abiertos encontrados:{Colors.RESET}\n")

        # Mostrar puertos en formato tabla
        print(f"{Colors.BOLD_YELLOW}Puerto\tServicio\t\tEstado{Colors.RESET}")
        print("-" * 50)

        for port in sorted(self.open_ports):
            service = self.services.get(port, 'Unknown')
            status = f"{Colors.GREEN}ABIERTO{Colors.RESET}"
            print(f"{port}\t{service:<20}{status}")

        print(f"\n{Colors.CYAN}[*] Tiempo de escaneo: {elapsed_time:.2f} segundos{Colors.RESET}")

def main(args):
    """Función principal llamada por snek.py"""
    parser = argparse.ArgumentParser(description="Escáner rápido de puertos y servicios")
    parser.add_argument('-t', '--target', required=True, help="Dirección IP o hostname objetivo")
    parser.add_argument('-p', '--ports', default='1-1000', help="Rango de puertos (ej: 1-1000 o 80,443,8080)")
    parser.add_argument('--timeout', type=float, default=1.0, help="Timeout de conexión en segundos (default: 1.0)")
    parser.add_argument('--threads', type=int, default=100, help="Número de hilos (default: 100)")
    parser.add_argument('-v', '--verbose', action='store_true', help="Modo verboso")
    parser.add_argument('--top-ports', type=int, help="Escanea los N puertos más comunes")

    # Si args está vacío, mostrar ayuda
    if not args:
        parser.print_help()
        return

    try:
        parsed_args = parser.parse_args(args)
    except SystemExit:
        return

    # Validar target
    utils = Utils()
    if not utils.is_valid_ip(parsed_args.target):
        try:
            # Intentar resolver hostname
            socket.gethostbyname(parsed_args.target)
        except socket.gaierror:
            print(f"{Colors.RED}[!] Error: Objetivo inválido o no resuelve: {parsed_args.target}{Colors.RESET}")
            return

    # Parsear puertos
    ports = []
    if parsed_args.top_ports:
        # Top 20 puertos más comunes
        common_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445,
                       993, 995, 1723, 3306, 3389, 5900, 8080]
        ports = common_ports[:parsed_args.top_ports]
    else:
        if '-' in parsed_args.ports:
            try:
                start, end = map(int, parsed_args.ports.split('-'))
                ports = list(range(start, min(end + 1, 65536)))
            except ValueError:
                print(f"{Colors.RED}[!] Error: Formato de puertos inválido{Colors.RESET}")
                return
        else:
            try:
                ports = [int(p.strip()) for p in parsed_args.ports.split(',') if p.strip()]
            except ValueError:
                print(f"{Colors.RED}[!] Error: Formato de puertos inválido{Colors.RESET}")
                return

    if not ports:
        print(f"{Colors.RED}[!] Error: No se especificaron puertos válidos{Colors.RESET}")
        return

    # Ejecutar escaneo
    scanner = PortScanner(
        target=parsed_args.target,
        ports=ports,
        timeout=parsed_args.timeout,
        threads=parsed_args.threads,
        verbose=parsed_args.verbose
    )
    scanner.scan()

if __name__ == "__main__":
    main(sys.argv[1:])
