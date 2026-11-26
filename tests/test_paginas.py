"""Tests de interfaz: cada página se renderiza sin excepciones.

AppTest ejecuta la app sin navegador, igual que el servidor de Streamlit,
y permite inspeccionar los elementos que se habrían mostrado.
"""

import pytest
from streamlit.testing.v1 import AppTest

from core.config import DIR_RAIZ
from servicios.contenido import obtener_perfil, obtener_proyecto_destacado

PAGINAS = [
    "app_pages/inicio.py",
    "app_pages/proyectos.py",
    "app_pages/sobre_mi.py",
    "app_pages/contacto.py",
]


def _app() -> AppTest:
    return AppTest.from_file(str(DIR_RAIZ / "app.py"), default_timeout=10)


@pytest.mark.parametrize("pagina", PAGINAS)
def test_pagina_sin_excepciones(pagina):
    at = _app().run()
    at.switch_page(pagina).run()
    assert not at.exception


def test_inicio_muestra_perfil_y_destacado():
    at = _app().run()
    perfil = obtener_perfil()
    destacado = obtener_proyecto_destacado()

    assert at.title[0].value == perfil.nombre
    subtitulos = [s.value for s in at.subheader]
    assert perfil.titular in subtitulos
    assert destacado is not None and destacado.titulo in subtitulos
