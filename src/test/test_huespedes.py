from src.huespedes import registrar_huesped, huespedes_db
from faker import Faker
import pytest
import re

fake = Faker("es_ES")


# ---------- Fixtures ----------

@pytest.fixture(autouse=True)
def limpiar_db():
    #Limpia la base de datos simulada antes de cada prueba,
    #evitando que un test afecte el resultado de otro
    huespedes_db.clear()
    yield


@pytest.fixture
def huesped_valido():
    #Genera datos ficticios (pero con formato realista) de un huésped
    #utilizando la librería Faker, evitando el uso de información real
    #se desempacara con **
    return {
        "nombre": fake.name(),
        "email": fake.email(),
        "telefono": fake.numerify("########"),
    }


# ---------- Pruebas de registro de huéspedes ----------
# Se realizarán pruebas parametrizadas para validar diferentes escenarios
# relacionados con los datos personales del huésped, generados con Faker.
# 1. Validar que el nombre no esté vacío.
# 2. Validar que el correo tenga un formato correcto.
# 3. Validar que el teléfono contenga solo números y largo mínimo.
# 4. Validar el registro exitoso de un huésped con datos válidos generados por Faker.
# 5. Validar que no se permita un huésped duplicado (mismo correo).
# 6. Validar el registro de múltiples huéspedes generados dinámicamente con Faker.
@pytest.mark.parametrize(
    "campo, valor_invalido, mensaje_esperado",
    [
        ("nombre", "   ", "El nombre es obligatorio y debe ser un texto."),
        ("email", "correo-sin-formato", "El correo electrónico no tiene un formato válido."),
        ("telefono", "abc123", "El teléfono debe contener solo números y al menos 8 dígitos."),
        ("telefono", "123", "El teléfono debe contener solo números y al menos 8 dígitos."),
    ],
    ids=[
        "nombre_vacio",
        "email_formato_invalido",
        "telefono_no_numerico",
        "telefono_muy_corto",
    ]
)
def test_registro_datos_invalidos(huesped_valido, campo, valor_invalido, mensaje_esperado):
    huesped_valido[campo] = valor_invalido
    with pytest.raises(ValueError, match=re.escape(mensaje_esperado)):
        registrar_huesped(**huesped_valido)


def test_registro_exitoso_con_datos_de_faker(huesped_valido):
    resultado = registrar_huesped(**huesped_valido)
    assert resultado["nombre"] == huesped_valido["nombre"]
    assert resultado["email"] == huesped_valido["email"]
    assert huesped_valido["email"] in huespedes_db


def test_registro_huesped_duplicado(huesped_valido):
    registrar_huesped(**huesped_valido)
    with pytest.raises(ValueError, match="Ya existe un huésped registrado"):
        registrar_huesped(**huesped_valido)


def test_multiples_huespedes_generados_con_faker():
    """Prueba de volumen: registra varios huéspedes con datos
    completamente generados por Faker, simulando un escenario
    con múltiples usuarios sin exponer información real."""
    for _ in range(5):
        datos = {
            "nombre": fake.name(),
            "email": fake.email(),
            "telefono": fake.numerify("########"),
        }
        registrar_huesped(**datos)
    assert len(huespedes_db) == 5