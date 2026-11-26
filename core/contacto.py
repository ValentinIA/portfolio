"""Mensajes del formulario de contacto: validación y construcción del email.

Todo lo que llega del formulario lo escribe un visitante anónimo, así que
se valida aquí, en el servidor, aunque el navegador ya haga sus propias
comprobaciones (esas se pueden saltar).
"""

import re
from dataclasses import dataclass
from email.message import EmailMessage

LIMITE_NOMBRE = 100
LIMITE_EMAIL = 254  # Longitud máxima de una dirección según el estándar (RFC 5321)
MINIMO_MENSAJE = 10
LIMITE_MENSAJE = 3000

# Comprobación sencilla a propósito: algo@algo.algo, sin espacios.
_PATRON_EMAIL = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")


@dataclass(frozen=True)
class MensajeContacto:
    nombre: str
    email: str
    mensaje: str


class ErrorValidacion(ValueError):
    """El mensaje no es válido. `errores` contiene un texto por cada problema."""

    def __init__(self, errores: list[str]):
        super().__init__("; ".join(errores))
        self.errores = errores


def validar_mensaje(nombre: str | None, email: str | None, mensaje: str | None) -> MensajeContacto:
    nombre = (nombre or "").strip()
    email = (email or "").strip()
    mensaje = (mensaje or "").strip()
    errores = []

    if not nombre:
        errores.append("Indica tu nombre.")
    elif len(nombre) > LIMITE_NOMBRE or "\n" in nombre or "\r" in nombre:
        # Un salto de línea en un campo que acaba en una cabecera del email
        # permitiría inyectar cabeceras nuevas (header injection).
        errores.append("El nombre no es válido.")

    if len(email) > LIMITE_EMAIL or not _PATRON_EMAIL.fullmatch(email):
        errores.append("Indica un email válido.")

    if len(mensaje) < MINIMO_MENSAJE:
        errores.append(f"El mensaje debe tener al menos {MINIMO_MENSAJE} caracteres.")
    elif len(mensaje) > LIMITE_MENSAJE:
        errores.append(f"El mensaje no puede superar los {LIMITE_MENSAJE} caracteres.")

    if errores:
        raise ErrorValidacion(errores)
    return MensajeContacto(nombre=nombre, email=email, mensaje=mensaje)


def construir_email(mensaje: MensajeContacto, remitente: str, destinatario: str) -> EmailMessage:
    """Crea el email que recibirás.

    Sale de tu propia cuenta (los servidores SMTP no permiten enviar en nombre
    de otra dirección); el email del visitante va en Reply-To, para que al
    pulsar "Responder" le contestes directamente.
    """
    email = EmailMessage()
    email["Subject"] = f"Portfolio · Mensaje de {mensaje.nombre}"
    email["From"] = remitente
    email["To"] = destinatario
    email["Reply-To"] = mensaje.email
    email.set_content(f"Nombre: {mensaje.nombre}\nEmail: {mensaje.email}\n\n{mensaje.mensaje}\n")
    return email
