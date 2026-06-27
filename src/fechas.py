from datetime import date


def validar_fechas(checkin, checkout):
    # Validar que la fecha de check-in no sea anterior a la actualidad
    if checkin < date.today():
        raise ValueError(
            "La fecha de check-in no puede ser anterior a la fecha actual"
            )
    # Validar que la fecha de check-out sea posterior a la fecha de check-in
    if checkout <= checkin:
        raise ValueError(
            "La fecha de check-out debe ser posterior a la fecha de check-in"
            )
    return True
