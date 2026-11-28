"""Carga y valida el contenido del portfolio desde archivos TOML.

Convierte los diccionarios que devuelve tomllib en los objetos de
core.modelos. Si falta un campo obligatorio o un valor no es válido,
lanza ErrorContenido indicando el archivo y el campo exactos, para que
el error aparezca al arrancar y no a mitad de una página.
"""

import tomllib
from pathlib import Path
from typing import Any

from core.config import DIR_CONTENIDO, DIR_STATIC
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


def es_url(valor: str) -> bool:
    return valor.startswith(("https://", "http://"))


def _validar_recurso(valor: str, contexto: str, dir_static: Path) -> str:
    """Una URL se acepta tal cual; una ruta local debe existir dentro de static/."""
    if es_url(valor):
        return valor
    ruta = Path(valor)
    # Nada de rutas con raíz ni "..": un recurso no puede salir de static/.
    # `anchor` detecta "/", "\" y "C:\" en cualquier sistema operativo
    # (en Windows, is_absolute() da False para "/etc/passwd").
    if ruta.anchor or ".." in ruta.parts:
        raise ErrorContenido(f"{contexto}: ruta no permitida '{valor}' (debe estar en static/)")
    if not (dir_static / ruta).is_file():
        raise ErrorContenido(f"{contexto}: no existe el archivo static/{valor}")
    return ruta.as_posix()


def _recurso_opcional(
    datos: dict[str, Any], campo: str, contexto: str, dir_static: Path
) -> str | None:
    valor = _texto_opcional(datos, campo, contexto)
    return None if valor is None else _validar_recurso(valor, contexto, dir_static)


def _recursos(
    datos: dict[str, Any], campo: str, contexto: str, dir_static: Path
) -> tuple[str, ...]:
    if campo not in datos:
        return ()
    valores = _lista_textos(datos, campo, contexto)
    return tuple(_validar_recurso(v, contexto, dir_static) for v in valores)


# --- Cargadores públicos ------------------------------------------------------


def cargar_perfil(directorio: Path = DIR_CONTENIDO, dir_static: Path = DIR_STATIC) -> Perfil:
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
        aprendiendo=_texto_opcional(datos, "aprendiendo", ctx),
        cv=_recurso_opcional(datos, "cv", ctx, dir_static),
    )


def _formaciones(
    datos: dict[str, Any], seccion: str, ctx: str, dir_static: Path
) -> tuple[Formacion, ...]:
    """Lee [[formacion]] o [[cursos]]: ambas secciones tienen los mismos campos."""
    c = f"{ctx} [[{seccion}]]"
    return tuple(
        Formacion(
            titulo=_texto(f, "titulo", c),
            centro=_texto(f, "centro", c),
            periodo=_texto(f, "periodo", c),
            descripcion=_texto_opcional(f, "descripcion", c),
            certificados=_recursos(f, "certificados", c, dir_static),
        )
        for f in _tablas(datos, seccion, ctx)
    )


def cargar_trayectoria(
    directorio: Path = DIR_CONTENIDO, dir_static: Path = DIR_STATIC
) -> Trayectoria:
    datos = _leer_toml(directorio / "trayectoria.toml")
    ctx = "trayectoria.toml"
    return Trayectoria(
        experiencia=tuple(
            Experiencia(
                empresa=_texto(e, "empresa", f"{ctx} [[experiencia]]"),
                puesto=_texto(e, "puesto", f"{ctx} [[experiencia]]"),
                periodo=_texto(e, "periodo", f"{ctx} [[experiencia]]"),
                descripcion=_texto(e, "descripcion", f"{ctx} [[experiencia]]"),
                certificados=_recursos(e, "certificados", f"{ctx} [[experiencia]]", dir_static),
                carta_recomendacion=_recurso_opcional(
                    e, "carta_recomendacion", f"{ctx} [[experiencia]]", dir_static
                ),
            )
            for e in _tablas(datos, "experiencia", ctx)
        ),
        formacion=_formaciones(datos, "formacion", ctx, dir_static),
        cursos=_formaciones(datos, "cursos", ctx, dir_static),
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


def cargar_proyectos(
    directorio: Path = DIR_CONTENIDO, dir_static: Path = DIR_STATIC
) -> tuple[Proyecto, ...]:
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
                docs_url=_recurso_opcional(p, "docs_url", ctx, dir_static),
                demo_url=_recurso_opcional(p, "demo_url", ctx, dir_static),
            )
        )

    slugs = [p.slug for p in proyectos]
    repetidos = sorted({s for s in slugs if slugs.count(s) > 1})
    if repetidos:
        raise ErrorContenido(f"proyectos.toml: slugs repetidos: {', '.join(repetidos)}")

    for slug in slugs:
        if not (directorio / "proyectos" / f"{slug}.md").exists():
            raise ErrorContenido(f"proyectos.toml: falta el detalle proyectos/{slug}.md")

    return tuple(proyectos)


def cargar_detalle_proyecto(slug: str, directorio: Path = DIR_CONTENIDO) -> str:
    """Devuelve el texto Markdown con el detalle de un proyecto."""
    ruta = directorio / "proyectos" / f"{slug}.md"
    if not ruta.exists():
        raise ErrorContenido(f"No existe el detalle del proyecto: proyectos/{slug}.md")
    return ruta.read_text(encoding="utf-8")
