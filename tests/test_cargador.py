"""Tests de carga y validación del contenido."""

import ast
from pathlib import Path

import pytest

from core.cargador import ErrorContenido, cargar_perfil, cargar_proyectos, cargar_trayectoria
from core.config import DIR_RAIZ
from core.modelos import EstadoProyecto

# --- El contenido real del portfolio carga sin errores ------------------------


def test_contenido_real_carga_correctamente():
    perfil = cargar_perfil()
    trayectoria = cargar_trayectoria()
    proyectos = cargar_proyectos()

    assert perfil.competencias
    assert trayectoria.experiencia and trayectoria.formacion and trayectoria.idiomas
    assert len(proyectos) == 3


def test_hay_exactamente_un_proyecto_destacado():
    destacados = [p for p in cargar_proyectos() if p.destacado]
    assert len(destacados) == 1


# --- La validación detecta contenido incorrecto -------------------------------


def _escribir(directorio: Path, nombre: str, texto: str) -> Path:
    (directorio / nombre).write_text(texto, encoding="utf-8")
    return directorio


PROYECTO_VALIDO = """
[[proyectos]]
slug = "demo"
titulo = "Demo"
categoria = "Pruebas"
resumen = "Resumen."
estado = "prototipo"
tecnologias = ["Python"]
"""


def test_proyecto_valido_con_campos_opcionales_ausentes(tmp_path):
    (proyecto,) = cargar_proyectos(_escribir(tmp_path, "proyectos.toml", PROYECTO_VALIDO))

    assert proyecto.estado is EstadoProyecto.PROTOTIPO
    assert proyecto.destacado is False
    assert proyecto.repo_url is None
    assert proyecto.demo_url is None


def test_falta_campo_obligatorio(tmp_path):
    toml = PROYECTO_VALIDO.replace('titulo = "Demo"\n', "")
    with pytest.raises(ErrorContenido, match="'titulo'"):
        cargar_proyectos(_escribir(tmp_path, "proyectos.toml", toml))


def test_estado_no_valido(tmp_path):
    toml = PROYECTO_VALIDO.replace('"prototipo"', '"terminado"')
    with pytest.raises(ErrorContenido, match="estado 'terminado' no válido"):
        cargar_proyectos(_escribir(tmp_path, "proyectos.toml", toml))


def test_slugs_repetidos(tmp_path):
    with pytest.raises(ErrorContenido, match="slugs repetidos: demo"):
        cargar_proyectos(_escribir(tmp_path, "proyectos.toml", PROYECTO_VALIDO * 2))


def test_toml_mal_formado(tmp_path):
    with pytest.raises(ErrorContenido, match="TOML mal formado"):
        cargar_proyectos(_escribir(tmp_path, "proyectos.toml", "slug = "))


def test_archivo_inexistente(tmp_path):
    with pytest.raises(ErrorContenido, match="No existe"):
        cargar_perfil(tmp_path)


# --- Regla de arquitectura: core/ no depende de Streamlit ---------------------


def test_core_no_importa_streamlit():
    for archivo in (DIR_RAIZ / "core").glob("*.py"):
        arbol = ast.parse(archivo.read_text(encoding="utf-8"))
        for nodo in ast.walk(arbol):
            if isinstance(nodo, ast.Import):
                modulos = [alias.name for alias in nodo.names]
            elif isinstance(nodo, ast.ImportFrom):
                modulos = [nodo.module or ""]
            else:
                continue
            assert not any(m.split(".")[0] == "streamlit" for m in modulos), archivo.name
