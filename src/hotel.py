"""
Sistema de Gestión de Reservas Hoteleras
Lógica de negocio: validación de fechas, cálculo de precio,
disponibilidad de habitaciones y registro de huéspedes.
"""
import re
from datetime import date


def validar_fechas(checkin: date, checkout: date) -> bool:
    """Valida que las fechas de una reserva sean lógicamente correctas."""
    if checkin >= checkout:
        raise ValueError("La fecha de check-out debe ser posterior al check-in")
    if checkin < date.today():
        raise ValueError("No se permiten fechas pasadas")
    return True


def calcular_precio_total(precio_noche: float, noches: int, descuento: float = 0) -> float:
    """Calcula el precio total de una reserva aplicando un descuento opcional."""
    if precio_noche <= 0:
        raise ValueError("El precio por noche debe ser mayor a 0")
    if noches <= 0:
        raise ValueError("El número de noches debe ser mayor a 0")
    if not 0 <= descuento <= 100:
        raise ValueError("El descuento debe estar entre 0 y 100")

    total = precio_noche * noches
    total -= total * (descuento / 100)
    return round(total, 2)


class Habitacion:
    """Representa una habitación del hotel y su disponibilidad."""

    def __init__(self, numero: int, disponible: bool = True):
        self.numero = numero
        self.disponible = disponible

    def reservar(self) -> bool:
        if not self.disponible:
            raise Exception("Habitación no disponible")
        self.disponible = False
        return True

    def liberar(self) -> bool:
        self.disponible = True
        return True


huespedes_db = {}


def registrar_huesped(nombre: str, email: str, telefono: str, documento: str) -> dict:
    """Registra un huésped validando el formato de sus datos personales."""
    if not nombre or not nombre.strip():
        raise ValueError("El nombre es obligatorio")

    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        raise ValueError("Email inválido")

    if not str(telefono).isdigit() or len(str(telefono)) < 8:
        raise ValueError("Teléfono inválido")

    documento = str(documento)
    if documento in huespedes_db:
        raise ValueError("El huésped ya está registrado")

    huespedes_db[documento] = {
        "nombre": nombre,
        "email": email,
        "telefono": telefono,
        "documento": documento,
    }
    return huespedes_db[documento]