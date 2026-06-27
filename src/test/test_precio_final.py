from src.precio_final import precio_final
import pytest
import re


# ---------- Pruebas de la función precio_final ----------
# Se realizarán pruebas parametrizadas para validar diferentes escenarios
# relacionados con la cantidad de noches, el precio por noche y el descuento.
# 1. Validar que la cantidad de noches no sea negativa.
# 2. Validar que la cantidad de noches no sea igual a 0.
# 3. Validar que el precio por noche no sea negativo.
# 4. Validar que el precio por noche no sea igual a 0.
# 5. Validar que el precio por noche no sea inferior a $40.000.
# 6. Validar que el precio por noche no sea superior a $120.000.
# 7. Validar que el descuento no sea inferior a 0%.
# 8. Validar que el descuento no sea superior al 100%.
# 9. Validar que la cantidad de noches sea un valor numérico.
# 10. Validar que el precio por noche sea un valor numérico.
# 11. Validar que el descuento sea un valor numérico.
# 12. Validar el cálculo del precio final para una reserva sin descuento.
# 13. Validar el cálculo del precio final para una reserva con un descuento del 15%.
# 14. Validar el cálculo del precio final para una reserva con un descuento del 100%.
# 15. Validar el cálculo del precio final utilizando el precio máximo permitido por noche.
from src.precio_final import precio_final
import pytest
import re


@pytest.mark.parametrize(
    "noches, precio_noche, descuento, resultado_o_mensaje, tipo_error",
    [
        (-1, 50000, 0, "La cantidad de noches debe ser como minimo 1", ValueError),
        (0, 50000, 0, "La cantidad de noches debe ser como minimo 1", ValueError),
        (2, -50000, 0, "El precio de la noche debe ser mayor a 0", ValueError),
        (2, 0, 0, "El precio de la noche debe ser mayor a 0", ValueError),
        (2, 39999, 0, "El rango de precios del hotel se encuentra entre $40.000 y $120.000", ValueError),
        (2, 120001, 0, "El rango de precios del hotel se encuentra entre $40.000 y $120.000", ValueError),
        (2, 50000, -1, "Descuento invalido", ValueError),
        (2, 50000, 101, "Descuento invalido", ValueError),
        ("dos", 50000, 0, "Ingrese números en el formulario", TypeError),
        (2, "cincuenta mil", 0, "Ingrese números en el formulario", TypeError),
        (2, 50000, False, "Ingrese números en el formulario", TypeError),
        (2, 50000, 0, 100000.0, None),
        (3, 80000, 15, 204000.0, None),
        (1, 40000, 100, 0.0, None),
        (2, 120000, 50, 120000.0, None),
    ],
    ids=[
        "noches_negativas",
        "noches_cero",
        "precio_negativo",
        "precio_cero",
        "precio_bajo_minimo",
        "precio_sobre_maximo",
        "descuento_negativo",
        "descuento_sobre_100",
        "noches_no_numerico",
        "precio_no_numerico",
        "descuento_booleano",
        "reserva_sin_descuento",
        "reserva_descuento_15",
        "reserva_descuento_100",
        "precio_maximo_valido",
    ]
)
def test_precio_final(noches, precio_noche, descuento, resultado_o_mensaje, tipo_error):
    if tipo_error is not None:
        with pytest.raises(tipo_error, match=re.escape(resultado_o_mensaje)):
            precio_final(noches, precio_noche, descuento)
    else:
        assert precio_final(noches, precio_noche, descuento) == resultado_o_mensaje