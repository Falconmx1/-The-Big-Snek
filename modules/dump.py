#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de extracción de metadatos de archivos (PDF, imágenes, documentos).
Uso: python dump.py -f documento.pdf
"""

import sys
import os
import argparse
import datetime
import struct
import re
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.colors import Colors
from core.logger import Logger
from core.utils import Utils

class MetaDumper:
    """Extractor de metadatos de archivos."""

    def __init__(self, filepath, verbose=False):
        self.filepath = filepath
        self.verbose = verbose
        self.logger = Logger()
        self.utils = Utils()
        self.metadata = {}

    def extract_pdf_metadata(self):
        """Extrae metadatos de archivos PDF."""
        try:
            with open(self.filepath, 'rb') as f:
                content = f.read()

            # Buscar metadatos en el PDF
            metadata = {}
            patterns = {
                'Title': r'/Title\s*\(([^)]*)\)',
                'Author': r'/Author\s*\(([^)]*)\)',
                'Subject': r'/Subject\s*\(([^)]*)\)',
                'Keywords': r'/Keywords\s*\(([^)]*)\)',
                'Creator': r'/Creator\s*\(([^)]*)\)',
                'Producer': r'/Producer\s*\(([^)]*)\)',
                'CreationDate': r'/CreationDate\s*\(([^)]*)\)',
                'ModDate': r'/ModDate\s*\(([^)]*)\)'
            }

            for key, pattern in patterns.items():
                match = re.search(pattern, content.decode('latin-1', errors='ignore'))
                if match:
                    value = match.group(1)
                    # Limpiar valores
                    value = value.replace('\\n', ' ').replace('\\r', ' ')
                    metadata[key] = value

            return metadata
        except Exception as e:
            if self.verbose:
                self.logger.error(f"Error extrayendo PDF: {e}")
            return {}

    def extract_image_metadata(self):
        """Extrae metadatos de imágenes."""
        try:
            metadata = {}
            img = Image.open(self.filepath)

            # Información básica
            metadata['Formato'] = img.format
            metadata['Modo'] = img.mode
            metadata['Tamaño'] = f"{img.width}x{img.height}"
            metadata['Paleta'] = img.palette is not None

            # EXIF data
            if hasattr(img, '_getexif'):
                exif = img._getexif()
                if exif:
                    for tag_id, value in exif.items():
                        tag = TAGS.get(tag_id, tag_id)
                        if tag == 'GPSInfo':
                            gps = {}
                            for gps_tag, gps_value in value.items():
                                gps_tag_name = GPSTAGS.get(gps_tag, gps_tag)
                                gps[gps_tag_name] = gps_value
                            metadata['GPSInfo'] = gps
                        else:
                            metadata[tag] = value

            return metadata
        except Exception as e:
            if self.verbose:
                self.logger.error(f"Error extrayendo imagen: {e}")
            return {}

    def extract_text_metadata(self):
        """Extrae metadatos de archivos de texto."""
        try:
            with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            metadata = {
                'Líneas': len(content.splitlines()),
                'Palabras': len(content.split()),
                'Caracteres': len(content),
                'Tamaño': os.path.getsize(self.filepath)
            }

            # Buscar metadatos en formato clave: valor
            for line in content.splitlines():
                if ':' in line and not line.startswith('#'):
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    if key and value and len(key) < 30:
                        metadata[key] = value

            return metadata
        except Exception as e:
            if self.verbose:
                self.logger.error(f"Error extrayendo texto: {e}")
            return {}

    def extract_file_metadata(self):
        """Extrae metadatos de archivos según su tipo."""
        file_ext = os.path.splitext(self.filepath)[1].lower()

        # Metadatos básicos
        self.metadata = {
            'Archivo': os.path.basename(self.filepath),
            'Tamaño': self.utils.human_readable_size(os.path.getsize(self.filepath)),
            'Última modificación': datetime.datetime.fromtimestamp(
                os.path.getmtime(self.filepath)).strftime('%Y-%m-%d %H:%M:%S')
        }

        # Extraer según tipo
        if file_ext == '.pdf':
            self.metadata.update(self.extract_pdf_metadata())
        elif file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
            self.metadata.update(self.extract_image_metadata())
        elif file_ext in ['.txt', '.log', '.cfg', '.conf', '.ini']:
            self.metadata.update(self.extract_text_metadata())
        else:
            # Intentar leer como texto
            try:
                self.metadata.update(self.extract_text_metadata())
            except:
                pass

        return self.metadata

    def print_metadata(self):
        """Imprime los metadatos extraídos."""
        print(f"\n{Colors.GREEN}╔════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.GREEN}║      METADATOS EXTRAÍDOS                 ║{Colors.RESET}")
        print(f"{Colors.GREEN}╚════════════════════════════════════════════╝{Colors.RESET}\n")

        for key, value in self.metadata.items():
            if isinstance(value, dict):
                print(f"{Colors.CYAN}{key}:{Colors.RESET}")
                for subkey, subvalue in value.items():
                    print(f"  {subkey}: {subvalue}")
            else:
                print(f"{Colors.CYAN}{key}:{Colors.RESET} {value}")

    def dump(self):
        """Ejecuta la extracción de metadatos."""
        if not self.utils.is_valid_file(self.filepath):
            self.logger.error(f"Archivo no válido: {self.filepath}")
            return {}

        if self.verbose:
            self.logger.info(f"Extrayendo metadatos de: {self.filepath}")

        self.extract_file_metadata()
        self.print_metadata()
        return self.metadata

def main(args):
    """Función principal llamada por snek.py"""
    parser = argparse.ArgumentParser(description="Extractor de metadatos de archivos")
    parser.add_argument('-f', '--file', required=True, help="Archivo a analizar")
    parser.add_argument('-v', '--verbose', action='store_true', help="Modo verboso")
    parser.add_argument('--output', help="Guardar metadatos en archivo JSON")

    if not args:
        parser.print_help()
        return

    try:
        parsed_args = parser.parse_args(args)
    except SystemExit:
        return

    if not os.path.exists(parsed_args.file):
        print(f"{Colors.RED}[!] Error: Archivo no encontrado{Colors.RESET}")
        return

    # Ejecutar extracción
    dumper = MetaDumper(parsed_args.file, verbose=parsed_args.verbose)
    metadata = dumper.dump()

    # Guardar salida
    if parsed_args.output and metadata:
        try:
            import json
            with open(parsed_args.output, 'w') as f:
                json.dump(metadata, f, indent=2, default=str)
            print(f"\n{Colors.GREEN}[+] Metadatos guardados en: {parsed_args.output}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Error guardando: {e}{Colors.RESET}")

if __name__ == "__main__":
    main(sys.argv[1:])
