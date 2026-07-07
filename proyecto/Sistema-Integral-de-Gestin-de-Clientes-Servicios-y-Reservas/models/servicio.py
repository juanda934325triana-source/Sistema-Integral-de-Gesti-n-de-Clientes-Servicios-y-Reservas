from abc import ABC, abstractmethod
from datetime import datetime
from exceptions.excepciones import ServicioOcupado

contador_servicios = 0

class ServicioBase(ABC):
    def __init__(self, nombre, descripcion, precio_base, limite=10):
        global contador_servicios
        contador_servicios += 1
        self.id = contador_servicios
        
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio_base = precio_base
        self.limite_reservas = limite
        self.disponible = True
        self._reservas_actuales = 0
        self.fecha_creacion = datetime.now()
    
    @abstractmethod
    def calcular_precio(self, horas, **datos):
        pass
    
    @abstractmethod
    def validar_datos(self, **datos):
        pass
    
    @abstractmethod
    def info(self):
        pass
    
    @abstractmethod
    def tipo(self):
        pass
    
    def reservar(self):
        if not self.disponible:
            raise ServicioOcupado(self.nombre)
        if self._reservas_actuales >= self.limite_reservas:
            raise ServicioOcupado(self.nombre)
        self._reservas_actuales += 1
    
    def liberar(self):
        if self._reservas_actuales > 0:
            self._reservas_actuales -= 1
    
    def reservas_actuales(self):
        return self._reservas_actuales
    
    def __str__(self):
        estado = "Disponible" if self.disponible else "No disponible"
        return f"[{self.tipo().upper()}] {self.nombre} - ${self.precio_base}/h - {estado}"