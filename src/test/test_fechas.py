from src.fechas import validar_fechas
from datetime import date, timedelta
import pytest
    
# ---------- Validación de fechas ----------
# Se realizarán pruebas parametrizadas para validar diferentes escenarios de fechas de check-in y check-out.
# 1. Validar que la fecha de check-in no sea anterior a la fecha actual.
# 2. Validar que la fecha de check-out sea posterior a la fecha de check-in.
# 3. Validar que la fecha de check-in y check-out sean iguales, lo cual no es permitido.
# 4. Validar que la fecha de check-in sea hoy mismo, lo cual es permitido.
# 5. Validar que la fecha de check-out sea hoy mismo, lo cual no es permitido si la fecha de check-in es posterior.
# 6. Validar que la fecha de check-in sea en el futuro y la fecha de check-out sea en el pasado, lo cual no es permitido.
# 7. Validar que la fecha de check-in sea mañana y la fecha de check-out sea pasado mañana, lo cual es permitido.
@pytest.mark.parametrize("checkin, checkout, mensaje_esperado, falla" ,[
    (date.today() - timedelta(days=1), date.today() + timedelta(days=2), "La fecha de check-in no puede ser anterior a la fecha actual",True),
    (date.today() + timedelta(days=2), date.today() + timedelta(days=1), "La fecha de check-out debe ser posterior a la fecha de check-in",True),
    (date.today() + timedelta(days=1), date.today() + timedelta(days=1), "La fecha de check-out debe ser posterior a la fecha de check-in",True),
    (date.today(), date.today() + timedelta(days=3), None,False),
    (date.today(), date.today(),"La fecha de check-out debe ser posterior a la fecha de check-in",True),
    (date.today(), date.today() - timedelta(days=1),"La fecha de check-out debe ser posterior a la fecha de check-in",True),
    (date.today() + timedelta(days=1), date.today() + timedelta(days=2), None,False)
],
    # ademas de agregar cada escenario, se puede agregar un id para identificar cada caso de prueba de manera más clara
    ids = [
        "checkin_pasado",
        "checkout_antes_checkin",
        "checkin_igual_checkout",
        "checkin_hoy_checkout_futuro",
        "checkin_hoy_checkout_hoy",
        "checkin_futuro_checkout_pasado",
        "checkin_futuro_checkout_mas_futuro"
    ]
)

def test_validar_fechas(checkin, checkout, mensaje_esperado, falla):
    if falla:
        with pytest.raises(ValueError, match = mensaje_esperado):
            validar_fechas(checkin, checkout)
    else:
        assert validar_fechas(checkin, checkout) is True
