import re
from datetime import datetime
from exceptions.excepciones import DatosClienteMalos

contador_clientes = 0

class Cliente:
    def __init__(self, nombre, email, telefono, tipo="regular"):
        global contador_clientes
        contador_clientes += 1
        self.id = contador_clientes
        
        self._nombre = None
        self._email = None
        self._telefono = None
        self._tipo = None
        self.activo = True
        self.fecha_registro = datetime.now()
        
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.tipo = tipo
    
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor):
        if not valor or len(valor.strip()) < 3:
            raise DatosClienteMalos("nombre", valor)
        if not all(c.isalpha() or c.isspace() for c in valor):
            raise DatosClienteMalos("nombre", valor)
        self._nombre = valor.strip()
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, valor):
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, valor):
            raise DatosClienteMalos("email", valor)
        self._email = valor.lower().strip()
    
    @property
    def telefono(self):
        return self._telefono
    
    @telefono.setter
    def telefono(self, valor):
        limpio = re.sub(r'[\s\-\(\)]', '', valor)
        if not limpio.isdigit() or len(limpio) < 7:
            raise DatosClienteMalos("telefono", valor)
        self._telefono = limpio
    
    @property
    def tipo(self):
        return self._tipo
    
    @tipo.setter
    def tipo(self, valor):
        valor = valor.lower().strip()
        if valor not in ['regular', 'premium', 'empresarial']:
            raise DatosClienteMalos("tipo", valor)
        self._tipo = valor
    
    def desactivar(self):
        self.activo = False
    
    def activar(self):
        self.activo = True
    
    def obtener_descuento(self):
        if self._tipo == "premium":
            return 10.0
        elif self._tipo == "empresarial":
            return 20.0
        return 0.0
    
    def __str__(self):
        estado = "Activo" if self.activo else "Inactivo"
        return f"{self.id} | {self._nombre} ({self._tipo}) - {self._email} - {estado}"