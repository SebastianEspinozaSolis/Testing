"""
Suite de pruebas automatizadas para el sistema de
Gestión de Reservas Hoteleras.
"""
from datetime import date, timedelta

import pytest
from faker import Faker

from src.hotel import (
    validar_fechas,
    calcular_precio_total,
    Habitacion,
    registrar_huesped,
    huespedes_db,
)

fake = Faker("es_ES")


# ---------- Fixtures ----------

@pytest.fixture(autouse=True)
def limpiar_db():
    """Limpia la base de datos simulada antes de cada test."""
    huespedes_db.clear()
    yield


@pytest.fixture
def huesped_valido():
    """Genera datos anonimizados de un huésped usando Faker."""
    return {
        "nombre": fake.name(),
        "email": fake.email(),
        "telefono": fake.msisdn()[:9],
        "documento": str(fake.unique.random_number(digits=8, fix_len=True)),
    }


# ---------- Validación de fechas ----------

def test_fechas_validas():
    checkin = date.today() + timedelta(days=1)
    checkout = date.today() + timedelta(days=3)
    assert validar_fechas(checkin, checkout) is True


def test_checkout_antes_de_checkin():
    checkin = date.today() + timedelta(days=3)
    checkout = date.today() + timedelta(days=1)
    with pytest.raises(ValueError, match="posterior"):
        validar_fechas(checkin, checkout)


def test_fecha_pasada():
    checkin = date.today() - timedelta(days=1)
    checkout = date.today() + timedelta(days=1)
    with pytest.raises(ValueError, match="pasadas"):
        validar_fechas(checkin, checkout)


def test_checkin_igual_checkout():
    hoy = date.today() + timedelta(days=1)
    with pytest.raises(ValueError):
        validar_fechas(hoy, hoy)


@pytest.mark.parametrize("dias_checkin, dias_checkout, debe_fallar", [
    (1, 3, False),   # rango válido normal
    (0, 2, False),   # check-in hoy mismo, válido
    (3, 1, True),    # checkout antes de checkin
    (-1, 2, True),   # checkin en el pasado
    (2, 2, True),    # checkin igual a checkout
])
def test_fechas_multiples_escenarios(dias_checkin, dias_checkout, debe_fallar):
    checkin = date.today() + timedelta(days=dias_checkin)
    checkout = date.today() + timedelta(days=dias_checkout)
    if debe_fallar:
        with pytest.raises(ValueError):
            validar_fechas(checkin, checkout)
    else:
        assert validar_fechas(checkin, checkout) is True


# ---------- Cálculo de precio total ----------

def test_precio_sin_descuento():
    assert calcular_precio_total(100, 3) == 300


def test_precio_con_descuento():
    assert calcular_precio_total(100, 3, descuento=10) == 270


@pytest.mark.parametrize("noches", [0, -1, -5])
def test_noches_invalidas(noches):
    with pytest.raises(ValueError, match="noches"):
        calcular_precio_total(100, noches)


@pytest.mark.parametrize("precio", [0, -50])
def test_precio_invalido(precio):
    with pytest.raises(ValueError, match="precio"):
        calcular_precio_total(precio, 2)


@pytest.mark.parametrize("descuento", [-10, 150])
def test_descuento_fuera_de_rango(descuento):
    with pytest.raises(ValueError, match="descuento"):
        calcular_precio_total(100, 2, descuento=descuento)


# ---------- Disponibilidad de habitaciones ----------

def test_reservar_habitacion_disponible():
    hab = Habitacion(101)
    assert hab.reservar() is True
    assert hab.disponible is False


def test_reservar_habitacion_no_disponible():
    hab = Habitacion(102, disponible=False)
    with pytest.raises(Exception, match="no disponible"):
        hab.reservar()


def test_liberar_habitacion():
    hab = Habitacion(103, disponible=False)
    assert hab.liberar() is True
    assert hab.disponible is True


@pytest.mark.parametrize("numero, disponible, debe_fallar", [
    (201, True, False),
    (202, True, False),
    (203, False, True),
    (204, False, True),
])
def test_disponibilidad_multiples_habitaciones(numero, disponible, debe_fallar):
    hab = Habitacion(numero, disponible=disponible)
    if debe_fallar:
        with pytest.raises(Exception, match="no disponible"):
            hab.reservar()
    else:
        assert hab.reservar() is True
        assert hab.disponible is False


# ---------- Registro de huéspedes (con Faker) ----------

def test_registro_exitoso(huesped_valido):
    resultado = registrar_huesped(**huesped_valido)
    assert resultado["nombre"] == huesped_valido["nombre"]
    assert huesped_valido["documento"] in huespedes_db


def test_registro_huesped_duplicado(huesped_valido):
    registrar_huesped(**huesped_valido)
    with pytest.raises(ValueError, match="ya está registrado"):
        registrar_huesped(**huesped_valido)


@pytest.mark.parametrize("email_invalido", [
    "sin-arroba.com",
    "@sinusuario.com",
    "espacio en@correo.com",
    "",
])
def test_email_invalido(huesped_valido, email_invalido):
    huesped_valido["email"] = email_invalido
    with pytest.raises(ValueError, match="Email inválido"):
        registrar_huesped(**huesped_valido)


@pytest.mark.parametrize("telefono_invalido", ["123", "abcdefgh", ""])
def test_telefono_invalido(huesped_valido, telefono_invalido):
    huesped_valido["telefono"] = telefono_invalido
    with pytest.raises(ValueError, match="Teléfono inválido"):
        registrar_huesped(**huesped_valido)


def test_nombre_vacio(huesped_valido):
    huesped_valido["nombre"] = "   "
    with pytest.raises(ValueError, match="nombre es obligatorio"):
        registrar_huesped(**huesped_valido)


def test_multiples_huespedes_con_datos_falsos():
    """Prueba de volumen con datos generados dinámicamente por Faker."""
    for _ in range(5):
        datos = {
            "nombre": fake.name(),
            "email": fake.email(),
            "telefono": fake.msisdn()[:9],
            "documento": str(fake.unique.random_number(digits=8, fix_len=True)),
        }
        registrar_huesped(**datos)
    assert len(huespedes_db) == 5