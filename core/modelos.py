"""Modelos de datos del portfolio.

Cada clase representa un tipo de contenido. Son inmutables (frozen=True):
una vez cargado, el contenido no cambia durante la ejecución.
"""

from dataclasses import dataclass
from enum import Enum


class EstadoProyecto(Enum):
    FUNCIONAL = "funcional"
    PROTOTIPO = "prototipo"
    PRUEBA_DE_CONCEPTO = "prueba_de_concepto"
    # Temporal: estado aún no confirmado. Debe desaparecer antes de cerrar la v1.
    PENDIENTE = "TODO"

    @property
    def etiqueta(self) -> str:
        etiquetas = {
            EstadoProyecto.FUNCIONAL: "Funcional",
            EstadoProyecto.PROTOTIPO: "Prototipo",
            EstadoProyecto.PRUEBA_DE_CONCEPTO: "Prueba de concepto",
            EstadoProyecto.PENDIENTE: "Estado pendiente de confirmar",
        }
        return etiquetas[self]


@dataclass(frozen=True)
class GrupoCompetencias:
    nombre: str
    tecnologias: tuple[str, ...]


@dataclass(frozen=True)
class Enlace:
    nombre: str
    url: str


@dataclass(frozen=True)
class Perfil:
    nombre: str
    titular: str
    ubicacion: str
    presentacion: str
    orientacion: tuple[str, ...]
    competencias: tuple[GrupoCompetencias, ...]
    enlaces: tuple[Enlace, ...]


@dataclass(frozen=True)
class Experiencia:
    empresa: str
    puesto: str
    periodo: str
    descripcion: str
    credencial_url: str | None = None


@dataclass(frozen=True)
class Formacion:
    titulo: str
    centro: str
    periodo: str
    descripcion: str | None = None
    credencial_url: str | None = None


@dataclass(frozen=True)
class Idioma:
    idioma: str
    nivel: str


@dataclass(frozen=True)
class Trayectoria:
    experiencia: tuple[Experiencia, ...]
    formacion: tuple[Formacion, ...]
    idiomas: tuple[Idioma, ...]


@dataclass(frozen=True)
class Proyecto:
    slug: str
    titulo: str
    categoria: str
    resumen: str
    estado: EstadoProyecto
    tecnologias: tuple[str, ...]
    destacado: bool = False
    repo_url: str | None = None
    docs_url: str | None = None
    # Reservado para la futura demo interactiva (FastAPI + modelo de ML).
    demo_url: str | None = None
