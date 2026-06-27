from src.habitaciones import Habitacion
import pytest
import re


# ---------- Pruebas de creación de Habitacion (__init__) ----------
# Se realizarán pruebas parametrizadas para validar diferentes escenarios
# relacionados con el número de habitación y el estado de disponibilidad.
# 1. Validar que el número de habitación no sea un texto (str).
# 2. Validar que el número de habitación no sea un decimal (float).
# 3. Validar que el número de habitación no sea igual a 0.
# 4. Validar que el número de habitación no sea negativo.
# 5. Validar que la disponibilidad no sea un valor no booleano.
# 6. Validar la creación correcta de una habitación con datos válidos.
@pytest.mark.parametrize(
    "numero, disponible, mensaje_esperado, tipo_error",
    [
        ("101", True, "El número de habitación debe ser un entero.", TypeError),
        (101.5, True, "El número de habitación debe ser un entero.", TypeError),
        (0, True, "El número de habitación debe ser mayor a 0.", ValueError),
        (-5, True, "El número de habitación debe ser mayor a 0.", ValueError),
        (101, "True", "La disponibilidad debe ser un valor booleano.", TypeError),
        (101, True, None, None),
    ],
    ids=[
        "numero_no_entero",
        "numero_float",
        "numero_cero",
        "numero_negativo",
        "disponible_no_booleano",
        "creacion_valida",
    ]
)
def test_creacion_habitacion(numero, disponible, mensaje_esperado, tipo_error):
    if tipo_error is not None:
        with pytest.raises(tipo_error, match=re.escape(mensaje_esperado)):
            Habitacion(numero, disponible)
    else:
        hab = Habitacion(numero, disponible)
        assert hab.numero == numero
        assert hab.disponible is True


# ---------- Pruebas del método reservar() ----------
# 7. Reservar una habitación disponible debe marcarla como no disponible.
# 8. Reservar una habitación ya reservada debe lanzar un error.
@pytest.mark.parametrize(
    "disponible_inicial, mensaje_esperado, falla",
    [
        (True, None, False),
        (False, "La habitación no se encuentra disponible.", True),
    ],
    ids=[
        "reservar_disponible",
        "reservar_no_disponible",
    ]
)
def test_reservar(disponible_inicial, mensaje_esperado, falla):
    hab = Habitacion(101, disponible_inicial)
    if falla:
        with pytest.raises(ValueError, match=re.escape(mensaje_esperado)):
            hab.reservar()
    else:
        assert hab.reservar() is True
        assert hab.disponible is False


# ---------- Pruebas del método liberar() ----------
# 9. Liberar una habitación reservada debe marcarla como disponible.
# 10. Liberar una habitación que ya está disponible debe lanzar un error.
@pytest.mark.parametrize(
    "disponible_inicial, mensaje_esperado, falla",
    [
        (False, None, False),
        (True, "La habitación ya se encuentra disponible.", True),
    ],
    ids=[
        "liberar_reservada",
        "liberar_ya_disponible",
    ]
)
def test_liberar(disponible_inicial, mensaje_esperado, falla):
    hab = Habitacion(101, disponible_inicial)
    if falla:
        with pytest.raises(ValueError, match=re.escape(mensaje_esperado)):
            hab.liberar()
    else:
        assert hab.liberar() is True
        assert hab.disponible is True