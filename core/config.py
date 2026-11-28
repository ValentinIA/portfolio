"""Rutas del proyecto, calculadas a partir de la ubicación de este archivo.

Así funcionan igual en local y en Streamlit Cloud, sin depender del
directorio desde el que se lance la aplicación.
"""

from pathlib import Path

DIR_RAIZ = Path(__file__).resolve().parent.parent
DIR_CONTENIDO = DIR_RAIZ / "content"
DIR_ASSETS = DIR_RAIZ / "assets"
# Archivos públicos servidos por Streamlit en /app/static/ (certificados, documentos).
DIR_STATIC = DIR_RAIZ / "static"
