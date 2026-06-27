class Habitacion:
    """Representa una habitación del hotel y su disponibilidad."""

    def __init__(self, numero: int, disponible: bool = True):

        if type(numero) is not int:
            raise TypeError("El número de habitación debe ser un entero.")

        if numero <= 0:
            raise ValueError(
                "El número de habitación debe ser mayor a 0."
            )

        if type(disponible) is not bool:
            raise TypeError(
                "La disponibilidad debe ser un valor booleano."
            )

        self.numero = numero
        self.disponible = disponible

    def reservar(self) -> bool:
        if not self.disponible:
            raise ValueError("La habitación no se encuentra disponible.")

        self.disponible = False
        return True

    def liberar(self) -> bool:
        if self.disponible:
            raise ValueError("La habitación ya se encuentra disponible.")

        self.disponible = True
        return True
