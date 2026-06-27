def precio_final(noches, precio_noche, descuento):
    # Calcula el precio de la reserva multiplicando precio de noche por noches
    # En caso de haber descuento, se aplica al precio total
    # Por ello validar que noches y precio_noche sean mayores a 0
    # y que descuento esté entre 0 y 100
    if (
            isinstance(noches, bool) or
            not isinstance(noches, (int, float)) or
            isinstance(precio_noche, bool) or
            not isinstance(precio_noche, (int, float)) or
            isinstance(descuento, bool) or
            not isinstance(descuento, (int, float))
    ):
        raise TypeError("Ingrese números en el formulario")
    if noches <= 0:
        raise ValueError(
            "La cantidad de noches debe ser como minimo 1"
            )
    if precio_noche <= 0:
        raise ValueError(
            "El precio de la noche debe ser mayor a 0"
            )
    # se colocara el caso de que el hotel tiene
    # como minimo valor de $40.000 y maximo $120.000
    elif precio_noche < 40000 or precio_noche > 120000:
        raise ValueError(
            "El rango de precios del hotel se encuentra "
            "entre $40.000 y $120.000"
            )
    if descuento < 0 or descuento > 100:
        raise ValueError(
            "Descuento invalido"
            )
    total = noches * precio_noche
    total = total - (total * descuento / 100)
    return round(total, 0)
