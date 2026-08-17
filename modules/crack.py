#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de fuerza bruta de hashes (MD5, SHA1, SHA256, WPA2).
Uso: python crack.py -h hash.txt -w wordlists/top1000.txt
"""

import sys
import os
import hashlib
import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.colors import Colors
from core.logger import Logger
from core.utils import Utils

class HashCracker:
    """Motor de crackeo de hashes optimizado para CPU."""

    def __init__(self, hash_file, wordlist, algo='md5', threads=4, verbose=False):
        self.hash_file = hash_file
        self.wordlist = wordlist
        self.algo = algo.lower()
        self.threads = threads
        self.verbose = verbose
        self.logger = Logger()
        self.utils = Utils()
        self.hashes = []
        self.cracked = {}

        # Mapeo de algoritmos soportados
        self.algorithms = {
            'md5': hashlib.md5,
            'sha1': hashlib.sha1,
            'sha256': hashlib.sha256,
            'sha512': hashlib.sha512,
            'ntlm': lambda s: hashlib.new('md4', s.encode('utf-16le')).hexdigest()
        }

    def load_hashes(self):
        """Carga los hashes desde el archivo."""
        content = self.utils.read_file_lines(self.hash_file)
        if not content:
            return False

        for line in content:
            # Intentar detectar formato "hash:password" ya crackeado
            if ':' in line:
                parts = line.split(':', 1)
                self.hashes.append(parts[0].strip())
                self.cracked[parts[0].strip()] = parts[1].strip()
            else:
                self.hashes.append(line.strip())

        if self.verbose:
            self.logger.info(f"Cargados {len(self.hashes)} hashes")
        return True

    def crack_hash(self, hash_value, word):
        """Intenta crackear un hash con una palabra específica."""
        try:
            hasher = self.algorithms.get(self.algo)
            if not hasher:
                self.logger.error(f"Algoritmo no soportado: {self.algo}")
                return None, None

            hash_calc = hasher(word.encode('utf-8')).hexdigest()

            if hash_calc.lower() == hash_value.lower():
                return hash_value, word
        except Exception:
            pass
        return None, None

    def crack_worker(self, hash_value, words):
        """Worker para procesar un hash con múltiples palabras."""
        for word in words:
            result, password = self.crack_hash(hash_value, word)
            if result:
                return result, password
        return None, None

    def crack(self):
        """Ejecuta el proceso de crackeo."""
        if not self.load_hashes():
            self.logger.error("No se pudieron cargar los hashes")
            return {}

        # Cargar wordlist
        words = self.utils.read_file_lines(self.wordlist)
        if not words:
            self.logger.error("No se pudo cargar la wordlist")
            return {}

        print(f"\n{Colors.CYAN}[*] Algoritmo: {self.algo.upper()}{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Hashes: {len(self.hashes)}{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Palabras: {len(words)}{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Hilos: {self.threads}{Colors.RESET}\n")

        start_time = time.time()
        cracked_count = 0

        # Dividir wordlist para threads
        chunk_size = max(1, len(words) // self.threads)
        word_chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]

        for i, hash_value in enumerate(self.hashes, 1):
            # Saltar si ya está crackeado
            if hash_value in self.cracked:
                if self.verbose:
                    self.logger.info(f"[{i}/{len(self.hashes)}] {hash_value[:16]}... ya crackeado")
                continue

            print(f"{Colors.YELLOW}[*] Probando hash {i}/{len(self.hashes)}: {hash_value[:16]}...{Colors.RESET}")

            found = False
            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                futures = []
                for chunk in word_chunks:
                    futures.append(executor.submit(self.crack_worker, hash_value, chunk))

                for future in as_completed(futures):
                    result, password = future.result()
                    if result:
                        self.cracked[hash_value] = password
                        print(f"{Colors.GREEN}[+] ¡CRACKEADO! {hash_value[:16]}... -> {password}{Colors.RESET}")
                        found = True
                        cracked_count += 1
                        break

            if not found:
                print(f"{Colors.RED}[-] No encontrado: {hash_value[:16]}...{Colors.RESET}")

        elapsed_time = time.time() - start_time
        self.print_results(elapsed_time, cracked_count)
        return self.cracked

    def print_results(self, elapsed_time, cracked_count):
        """Muestra los resultados del crackeo."""
        print(f"\n{Colors.GREEN}╔════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.GREEN}║         RESULTADOS DEL CRACKEO           ║{Colors.RESET}")
        print(f"{Colors.GREEN}╚════════════════════════════════════════════╝{Colors.RESET}")

        if cracked_count > 0:
            print(f"\n{Colors.CYAN}[+] {cracked_count}/{len(self.hashes)} hashes crackeados:{Colors.RESET}\n")
            for hash_val, password in self.cracked.items():
                print(f"{Colors.GREEN}{hash_val}{Colors.RESET} -> {Colors.YELLOW}{password}{Colors.RESET}")
        else:
            print(f"\n{Colors.RED}[!] No se pudo crackear ningún hash.{Colors.RESET}")

        print(f"\n{Colors.CYAN}[*] Tiempo: {elapsed_time:.2f} segundos{Colors.RESET}")

def main(args):
    """Función principal llamada por snek.py"""
    parser = argparse.ArgumentParser(description="Fuerza bruta de hashes (MD5, SHA1, SHA256, WPA2)")
    parser.add_argument('-h', '--hash-file', required=True, help="Archivo con los hashes a crackear")
    parser.add_argument('-w', '--wordlist', default='wordlists/top1000.txt', help="Archivo con la wordlist")
    parser.add_argument('-a', '--algo', default='md5', choices=['md5', 'sha1', 'sha256', 'sha512', 'ntlm'],
                       help="Algoritmo de hash (default: md5)")
    parser.add_argument('--threads', type=int, default=4, help="Número de hilos (default: 4)")
    parser.add_argument('-v', '--verbose', action='store_true', help="Modo verboso")
    parser.add_argument('--generate', help="Genera un hash de ejemplo: --generate md5 password123")

    if not args:
        parser.print_help()
        return

    try:
        parsed_args = parser.parse_args(args)
    except SystemExit:
        return

    # Generar hash de ejemplo
    if parsed_args.generate:
        try:
            algo, password = parsed_args.generate.split(' ', 1)
            hasher = hashlib.new(algo.lower())
            hasher.update(password.encode('utf-8'))
            print(f"{Colors.GREEN}[+] Hash {algo.upper()}: {hasher.hexdigest()}{Colors.RESET}")
            print(f"{Colors.YELLOW}[*] Contraseña: {password}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Error generando hash: {e}{Colors.RESET}")
        return

    # Verificar archivos
    if not os.path.exists(parsed_args.hash_file):
        print(f"{Colors.RED}[!] Error: Archivo de hashes no encontrado{Colors.RESET}")
        return

    # Wordlist por defecto
    if parsed_args.wordlist == 'wordlists/top1000.txt':
        default_wordlist = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                       'wordlists', 'top1000.txt')
        if os.path.exists(default_wordlist):
            parsed_args.wordlist = default_wordlist

    if not os.path.exists(parsed_args.wordlist):
        print(f"{Colors.RED}[!] Error: Wordlist no encontrada: {parsed_args.wordlist}{Colors.RESET}")
        return

    # Ejecutar crackeo
    cracker = HashCracker(
        hash_file=parsed_args.hash_file,
        wordlist=parsed_args.wordlist,
        algo=parsed_args.algo,
        threads=parsed_args.threads,
        verbose=parsed_args.verbose
    )
    cracker.crack()

if __name__ == "__main__":
    main(sys.argv[1:])
