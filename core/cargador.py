"""Carga y valida el contenido del portfolio desde archivos TOML.

Convierte los diccionarios que devuelve tomllib en los objetos de
core.modelos. Si falta un campo obligatorio o un valor no es válido,
lanza ErrorContenido indicando el archivo y el campo exactos, para que
el error aparezca al arrancar y no a mitad de una página.
"""

import tomllib
from pathlib import Path
from typing import Any

from core.config import DIR_CONTENIDO
from core.modelos import (
    Enlace,
    EstadoProyecto,
    Experiencia,
    Formacion,
    GrupoCompetencias,
    Idioma,
    Perfil,
    Proyecto,
    Trayectoria,
)


class ErrorContenido(ValueError):
    """El contenido de un archivo TOML no es válido."""


# --- Utilidades de lectura y validación ---------------------------------------


def _leer_toml(ruta: Path) -> dict[str, Any]:
    if not ruta.exists():
        raise ErrorContenido(f"No existe el archivo de contenido: {ruta}")
    try:
        with ruta.open("rb") as archivo:
            return tomllib.load(archivo)
    except tomllib.TOMLDecodeError as error:
        raise ErrorContenido(f"{ruta.name}: TOML mal formado ({error})") from error


def _texto(datos: dict[str, Any], campo: str, contexto: str) -> str:
    valor = datos.get(campo)
    if not isinstance(valor, str) or not valor.strip():
        raise ErrorContenido(f"{contexto}: falta el campo de texto '{campo}'")
    return valor.strip()


def _texto_opcional(datos: dict[str, Any], campo: str, contexto: str) -> str | None:
    if campo not in datos:
        return None
    return _texto(datos, campo, contexto)


def _lista_textos(datos: dict[str, Any], campo: str, contexto: str) -> tuple[str, ...]:
    valor = datos.get(campo)
    if not isinstance(valor, list) or not valor or not all(isinstance(v, str) for v in valor):
        raise ErrorContenido(f"{contexto}: '{campo}' debe ser una lista de textos no vacía")
    return tuple(v.strip() for v in valor)


def _tablas(datos: dict[str, Any], campo: str, contexto: str) -> list[dict[str, Any]]:
    valor = datos.get(campo)
    if not isinstance(valor, list) or not valor:
        raise ErrorContenido(f"{contexto}: falta la sección '[[{campo}]]'")
    return valor


# --- Cargadores públicos ------------------------------------------------------


def cargar_perfil(directorio: Path = DIR_CONTENIDO) -> Perfil:
    datos = _leer_toml(directorio / "perfil.toml")
    ctx = "perfil.toml"
    return Perfil(
        nombre=_texto(datos, "nombre", ctx),
        titular=_texto(datos, "titular", ctx),
        ubicacion=_texto(datos, "ubicacion", ctx),
        presentacion=_texto(datos, "presentacion", ctx),
        orientacion=_lista_textos(datos, "orientacion", ctx),
        competencias=tuple(
            GrupoCompetencias(
                nombre=_texto(grupo, "nombre", f"{ctx} [[competencias]]"),
                tecnologias=_lista_textos(grupo, "tecnologias", f"{ctx} [[competencias]]"),
            )
            for grupo in _tablas(datos, "competencias", ctx)
        ),
        enlaces=tuple(
            Enlace(
                nombre=_texto(enlace, "nombre", f"{ctx} [[enlaces]]"),
                url=_texto(enlace, "url", f"{ctx} [[enlaces]]"),
            )
            for enlace in _tablas(datos, "enlaces", ctx)
        ),
    )


def cargar_trayectoria(directorio: Path = DIR_CONTENIDO) -> Trayectoria:
    datos = _leer_toml(directorio / "trayectoria.toml")
    ctx = "trayectoria.toml"
    return Trayectoria(
        experiencia=tuple(
            Experiencia(
                empresa=_texto(e, "empresa", f"{ctx} [[experiencia]]"),
                puesto=_texto(e, "puesto", f"{ctx} [[experiencia]]"),
                periodo=_texto(e, "periodo", f"{ctx} [[experiencia]]"),
                descripcion=_texto(e, "descripcion", f"{ctx} [[experiencia]]"),
                credencial_url=_texto_opcional(e, "credencial_url", f"{ctx} [[experiencia]]"),
            )
            for e in _tablas(datos, "experiencia", ctx)
        ),
        formacion=tuple(
            Formacion(
                titulo=_texto(f, "titulo", f"{ctx} [[formacion]]"),
                centro=_texto(f, "centro", f"{ctx} [[formacion]]"),
                periodo=_texto(f, "periodo", f"{ctx} [[formacion]]"),
                descripcion=_texto_opcional(f, "descripcion", f"{ctx} [[formacion]]"),
                credencial_url=_texto_opcional(f, "credencial_url", f"{ctx} [[formacion]]"),
            )
            for f in _tablas(datos, "formacion", ctx)
        ),
        idiomas=tuple(
            Idioma(
                idioma=_texto(i, "idioma", f"{ctx} [[idiomas]]"),
                nivel=_texto(i, "nivel", f"{ctx} [[idiomas]]"),
            )
            for i in _tablas(datos, "idiomas", ctx)
        ),
    )


def _estado(datos: dict[str, Any], contexto: str) -> EstadoProyecto:
    valor = _texto(datos, "estado", contexto)
    try:
        return EstadoProyecto(valor)
    except ValueError:
        validos = ", ".join(e.value for e in EstadoProyecto)
        raise ErrorContenido(
            f"{contexto}: estado '{valor}' no válido. Usa uno de: {validos}"
        ) from None


def cargar_proyectos(directorio: Path = DIR_CONTENIDO) -> tuple[Proyecto, ...]:
    datos = _leer_toml(directorio / "proyectos.toml")
    proyectos = []
    for indice, p in enumerate(_tablas(datos, "proyectos", "proyectos.toml"), start=1):
        ctx = f"proyectos.toml (proyecto {indice})"
        destacado = p.get("destacado", False)
        if not isinstance(destacado, bool):
            raise ErrorContenido(f"{ctx}: 'destacado' debe ser true o false")
        proyectos.append(
            Proyecto(
                slug=_texto(p, "slug", ctx),
                titulo=_texto(p, "titulo", ctx),
                categoria=_texto(p, "categoria", ctx),
                resumen=_texto(p, "resumen", ctx),
                estado=_estado(p, ctx),
                tecnologias=_lista_textos(p, "tecnologias", ctx),
                destacado=destacado,
                repo_url=_texto_opcional(p, "repo_url", ctx),
                docs_url=_texto_opcional(p, "docs_url", ctx),
                demo_url=_texto_opcional(p, "demo_url", ctx),
            )
        )

    slugs = [p.slug for p in proyectos]
    repetidos = sorted({s for s in slugs if slugs.count(s) > 1})
    if repetidos:
        raise ErrorContenido(f"proyectos.toml: slugs repetidos: {', '.join(repetidos)}")

    return tuple(proyectos)
