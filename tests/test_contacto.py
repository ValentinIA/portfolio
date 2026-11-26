"""Tests del formulario de contacto: validación, email y flujo en la página."""

import pytest
from streamlit.testing.v1 import AppTest

from core.config import DIR_RAIZ
from core.contacto import ErrorValidacion, construir_email, validar_mensaje
from servicios import correo

VALIDO = {"nombre": "Ana", "email": "ana@empresa.com", "mensaje": "Hola, me interesa tu perfil."}

# --- Validación (core) ---------------------------------------------------------


def test_mensaje_valido_se_normaliza():
    m = validar_mensaje("  Ana ", " ana@empresa.com ", "  Hola, me interesa tu perfil.  ")
    assert (m.nombre, m.email, m.mensaje) == ("Ana", "ana@empresa.com", VALIDO["mensaje"])


@pytest.mark.parametrize(
    ("campo", "valor", "error"),
    [
        ("nombre", "", "Indica tu nombre."),
        ("nombre", "Ana\r\nBcc: spam@x.com", "El nombre no es válido."),
        ("email", "no-es-un-email", "Indica un email válido."),
        ("email", "ana@empresa.com\nBcc: x@y.z", "Indica un email válido."),
        ("mensaje", "Hola", "al menos"),
        ("mensaje", "x" * 3001, "no puede superar"),
    ],
)
def test_validacion_detecta_errores(campo, valor, error):
    datos = {**VALIDO, campo: valor}
    with pytest.raises(ErrorValidacion) as exc:
        validar_mensaje(**datos)
    assert any(error in e for e in exc.value.errores)


def test_email_sale_de_tu_cuenta_y_responde_al_visitante():
    email = construir_email(validar_mensaje(**VALIDO), "yo@gmail.com", "buzon@gmail.com")
    assert email["From"] == "yo@gmail.com"
    assert email["To"] == "buzon@gmail.com"
    assert email["Reply-To"] == "ana@empresa.com"
    assert "Hola, me interesa tu perfil." in email.get_content()


# --- Flujo en la página --------------------------------------------------------

SECRETOS = {
    "servidor": "smtp.ejemplo.com",
    "puerto": 465,
    "usuario": "yo@ejemplo.com",
    "contrasena": "secreta",
}


def _contacto(secretos: dict | None = None) -> AppTest:
    at = AppTest.from_file(str(DIR_RAIZ / "app.py"), default_timeout=10)
    if secretos is not None:
        at.secrets["contacto"] = secretos
    at.run()
    return at.switch_page("app_pages/contacto.py").run()


def _rellenar_y_enviar(at: AppTest, **campos) -> AppTest:
    datos = {**VALIDO, **campos}
    at.text_input(key="contacto_nombre").input(datos["nombre"])
    at.text_input(key="contacto_email").input(datos["email"])
    at.text_area(key="contacto_mensaje").input(datos["mensaje"])
    return at.button(key="contacto_enviar").click().run()


def test_sin_secretos_no_muestra_formulario():
    at = _contacto()
    assert not at.exception
    assert len(at.info) == 1
    assert len(at.text_input) == 0


def test_envio_correcto(monkeypatch):
    enviados = []
    monkeypatch.setattr(correo, "enviar_mensaje", lambda m, c: enviados.append((m, c)))

    at = _rellenar_y_enviar(_contacto(SECRETOS))

    assert not at.exception
    assert len(enviados) == 1
    assert enviados[0][0].email == VALIDO["email"]
    assert enviados[0][1].destinatario == "yo@ejemplo.com"  # por defecto, el usuario
    assert len(at.success) == 1


def test_error_de_validacion_no_envia(monkeypatch):
    enviados = []
    monkeypatch.setattr(correo, "enviar_mensaje", lambda m, c: enviados.append(m))

    at = _rellenar_y_enviar(_contacto(SECRETOS), mensaje="corto")

    assert enviados == []
    assert len(at.error) == 1


def test_fallo_de_envio_muestra_error_generico(monkeypatch):
    def falla(m, c):
        raise correo.ErrorEnvio("535 credenciales incorrectas")

    monkeypatch.setattr(correo, "enviar_mensaje", falla)

    at = _rellenar_y_enviar(_contacto(SECRETOS))

    assert len(at.error) == 1
    assert "535" not in at.error[0].value  # el detalle técnico no llega al visitante


def test_espera_entre_envios(monkeypatch):
    def falla(m, c):
        raise correo.ErrorEnvio("caído")

    monkeypatch.setattr(correo, "enviar_mensaje", falla)

    at = _rellenar_y_enviar(_contacto(SECRETOS))
    at = _rellenar_y_enviar(at)

    assert len(at.warning) == 1
