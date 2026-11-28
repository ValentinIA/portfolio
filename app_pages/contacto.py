"""Página de contacto: enlaces profesionales y formulario de contacto."""

import time

import streamlit as st

from components.enlaces import botones_enlaces
from core.contacto import (
    LIMITE_EMAIL,
    LIMITE_MENSAJE,
    LIMITE_NOMBRE,
    ErrorValidacion,
    validar_mensaje,
)
from servicios import correo
from servicios.contenido import obtener_perfil

# Límite anti-spam por sesión de navegador.
MAX_ENVIOS_POR_SESION = 3
ESPERA_ENTRE_ENVIOS_S = 60

st.session_state.setdefault("contacto_envios", [])
st.session_state.setdefault("contacto_enviado", False)

perfil = obtener_perfil()

st.title("Contacto", anchor=False)
st.markdown("¿Tienes una oferta o quieres comentar algún proyecto? Escríbeme.")

# Formulario (izquierda) y enlaces profesionales (derecha).
col_formulario, col_enlaces = st.columns([3, 2], gap="large")

with col_enlaces:
    st.header("Enlaces", anchor=False)
    with st.container(horizontal=True):
        botones_enlaces(perfil.enlaces, perfil.cv)

with col_formulario:
    st.header("Envíame un mensaje", anchor=False)

    config = correo.obtener_config()

    if config is None:
        st.info(
            "El formulario de contacto estará disponible próximamente. "
            "Mientras tanto, puedes escribirme por LinkedIn.",
            icon=":material/schedule:",
        )

    elif st.session_state.contacto_enviado:
        st.success(
            "Te responderé lo antes posible al email que has indicado.",
            title="Mensaje enviado",
            icon=":material/check_circle:",
        )
        if st.button("Enviar otro mensaje", key="contacto_otro"):
            st.session_state.contacto_enviado = False
            st.rerun()

    else:
        with st.form("contacto_formulario"):
            nombre = st.text_input(
                "Nombre", max_chars=LIMITE_NOMBRE, required=True, key="contacto_nombre"
            )
            email = st.text_input(
                "Email",
                type="email",
                max_chars=LIMITE_EMAIL,
                required=True,
                help="Solo lo usaré para responderte.",
                key="contacto_email",
            )
            mensaje = st.text_area(
                "Mensaje",
                max_chars=LIMITE_MENSAJE,
                required=True,
                height=180,
                key="contacto_mensaje",
            )
            enviado = st.form_submit_button(
                "Enviar", type="primary", icon=":material/send:", key="contacto_enviar"
            )

        if enviado:
            ahora = time.monotonic()
            envios = st.session_state.contacto_envios
            if len(envios) >= MAX_ENVIOS_POR_SESION:
                st.warning("Has alcanzado el máximo de mensajes. Puedes escribirme por LinkedIn.")
            elif envios and ahora - envios[-1] < ESPERA_ENTRE_ENVIOS_S:
                st.warning("Espera un minuto antes de enviar otro mensaje.")
            else:
                try:
                    datos = validar_mensaje(nombre, email, mensaje)
                except ErrorValidacion as error:
                    st.error(
                        "\n".join(f"- {e}" for e in error.errores), title="Revisa el formulario"
                    )
                else:
                    envios.append(ahora)  # Cuenta cada intento, también los fallidos.
                    try:
                        with st.spinner("Enviando..."):
                            correo.enviar_mensaje(datos, config)
                    except correo.ErrorEnvio:
                        # El detalle técnico no se muestra al visitante.
                        st.error(
                            "No se ha podido enviar el mensaje. Inténtalo más tarde "
                            "o escríbeme por LinkedIn."
                        )
                    else:
                        st.session_state.contacto_enviado = True
                        st.rerun()
