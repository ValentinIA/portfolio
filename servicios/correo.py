"""Envío de los mensajes del formulario por SMTP.

Usa smtplib (biblioteca estándar): sin dependencias nuevas ni servicios de
terceros que guarden los mensajes. Las credenciales viven en st.secrets
(.streamlit/secrets.toml en local, panel "Secrets" en Streamlit Cloud),
nunca en el código ni en el repositorio.
"""

import smtplib
from dataclasses import dataclass

import streamlit as st

from core.contacto import MensajeContacto, construir_email


@dataclass(frozen=True)
class ConfigCorreo:
    servidor: str
    puerto: int
    usuario: str
    contrasena: str
    destinatario: str


class ErrorEnvio(Exception):
    """No se pudo enviar el mensaje (servidor caído, credenciales, red...)."""


def obtener_config() -> ConfigCorreo | None:
    """Lee la configuración de los secretos. None si no está configurada."""
    try:
        s = st.secrets["contacto"]
        return ConfigCorreo(
            servidor=s["servidor"],
            puerto=int(s["puerto"]),
            usuario=s["usuario"],
            contrasena=s["contrasena"],
            destinatario=s.get("destinatario", s["usuario"]),
        )
    # FileNotFoundError: no hay archivo de secretos · KeyError: falta una clave
    # ValueError/TypeError: un valor con formato incorrecto (p. ej. el puerto)
    except (FileNotFoundError, KeyError, ValueError, TypeError):
        return None


def enviar_mensaje(mensaje: MensajeContacto, config: ConfigCorreo) -> None:
    email = construir_email(mensaje, remitente=config.usuario, destinatario=config.destinatario)
    try:
        # SMTP_SSL: la conexión va cifrada desde el principio (puerto 465).
        with smtplib.SMTP_SSL(config.servidor, config.puerto, timeout=15) as smtp:
            smtp.login(config.usuario, config.contrasena)
            smtp.send_message(email)
    except (smtplib.SMTPException, OSError) as error:
        raise ErrorEnvio(str(error)) from error
