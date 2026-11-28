"""Tests de interfaz: cada página se renderiza sin excepciones.

AppTest ejecuta la app sin navegador, igual que el servidor de Streamlit,
y permite inspeccionar los elementos que se habrían mostrado.
"""

import pytest
from streamlit.testing.v1 import AppTest

from core.config import DIR_RAIZ
from servicios.contenido import (
    obtener_perfil,
    obtener_proyecto_destacado,
    obtener_proyectos,
    obtener_trayectoria,
)

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


def _proyectos(slug: str | None = None) -> AppTest:
    at = _app().run()
    at.switch_page("app_pages/proyectos.py")
    if slug is not None:
        at.query_params["p"] = slug
    return at.run()


def test_proyectos_listado_muestra_todos():
    at = _proyectos()
    titulos = [s.value for s in at.subheader]
    assert at.title[0].value == "Proyectos"
    assert all(p.titulo in titulos for p in obtener_proyectos())


def test_proyectos_detalle_por_slug():
    at = _proyectos("buypilot")
    assert not at.exception
    assert at.title[0].value == "BuyPilot"
    assert any("Trabajo realizado" in m.value for m in at.markdown)


def test_proyectos_slug_inexistente_muestra_aviso_y_listado():
    at = _proyectos("no-existe")
    assert not at.exception
    assert len(at.warning) == 1
    assert at.title[0].value == "Proyectos"


def test_sobre_mi_muestra_toda_la_trayectoria():
    at = _app().run()
    at.switch_page("app_pages/sobre_mi.py").run()
    trayectoria = obtener_trayectoria()
    textos = " ".join(m.value for m in at.markdown) + " ".join(c.value for c in at.caption)

    assert not at.exception
    for e in trayectoria.experiencia:
        assert e.puesto in textos and e.empresa in textos
    for f in (*trayectoria.formacion, *trayectoria.cursos):
        assert f.titulo in textos and f.centro in textos
    for i in trayectoria.idiomas:
        assert i.idioma in textos

    certificados = [
        c
        for x in (*trayectoria.experiencia, *trayectoria.formacion, *trayectoria.cursos)
        for c in x.certificados
    ]
    enlaces = [e.proto for e in at.get("link_button") if "certificado" in e.proto.label]
    assert len(enlaces) == len(certificados)
    # Los archivos propios se enlazan a través del servidor estático de la app.
    assert all(e.url.startswith(("app/static/", "http")) for e in enlaces)
