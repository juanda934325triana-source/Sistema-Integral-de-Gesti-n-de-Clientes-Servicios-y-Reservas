import re

def validar_email(email):
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(patron, email):
        return True
    return False

def validar_telefono(telefono):
    limpio = re.sub(r'[\s\-\(\)]', '', telefono)
    if limpio.isdigit() and len(limpio) >= 7:
        return True
    return False

def validar_nombre(nombre):
    if not nombre:
        return False
    nombre = nombre.strip()
    if len(nombre) < 3:
        return False
    for c in nombre:
        if not (c.isalpha() or c.isspace()):
            return False
    return True