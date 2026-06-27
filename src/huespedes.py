import re

# Base de datos simulada en memoria (sin persistencia real)
huespedes_db = {}


def registrar_huesped(nombre, email, telefono):
    """Registra un huésped validando el formato de sus datos personales."""

    if not isinstance(nombre, str) or not nombre.strip():
        raise ValueError("El nombre es obligatorio y debe ser un texto.")

    if not isinstance(email, str) or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        raise ValueError("El correo electrónico no tiene un formato válido.")

    if not isinstance(telefono, str) or not telefono.isdigit() or len(telefono) < 8:
        raise ValueError("El teléfono debe contener solo números y al menos 8 dígitos.")

    if email in huespedes_db:
        raise ValueError("Ya existe un huésped registrado con ese correo.")

    huespedes_db[email] = {
        "nombre": nombre,
        "email": email,
        "telefono": telefono,
    }
    return huespedes_db[email]
