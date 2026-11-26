"""Acceso cacheado al contenido del portfolio.

Streamlit vuelve a ejecutar la página entera en cada interacción. Con
st.cache_data los archivos TOML se leen una sola vez por proceso y las
siguientes ejecuciones reutilizan el resultado.

Este módulo existe para que core/ siga sin depender de Streamlit: core/
sabe cargar el contenido; aquí solo decidimos cachearlo.

Nota: si editas un TOML con la app en marcha, limpia la caché
(menú ⋮ > "Clear cache", o tecla C) o reinicia la app para ver el cambio.
"""

import streamlit as st

from core.cargador import (
    cargar_detalle_proyecto,
    cargar_perfil,
    cargar_proyectos,
    cargar_trayectoria,
)
from core.modelos import Perfil, Proyecto, Trayectoria


@st.cache_data
def obtener_perfil() -> Perfil:
    return cargar_perfil()


@st.cache_data
def obtener_trayectoria() -> Trayectoria:
    return cargar_trayectoria()


@st.cache_data
def obtener_proyectos() -> tuple[Proyecto, ...]:
    return cargar_proyectos()


@st.cache_data
def obtener_detalle_proyecto(slug: str) -> str:
    return cargar_detalle_proyecto(slug)


def obtener_proyecto_destacado() -> Proyecto | None:
    return next((p for p in obtener_proyectos() if p.destacado), None)


def buscar_proyecto(slug: str | None) -> Proyecto | None:
    return next((p for p in obtener_proyectos() if p.slug == slug), None)
