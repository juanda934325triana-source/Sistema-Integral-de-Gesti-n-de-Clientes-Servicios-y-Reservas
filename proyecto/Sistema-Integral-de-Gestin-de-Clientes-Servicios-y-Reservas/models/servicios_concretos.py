from models.servicio import ServicioBase
from exceptions.excepciones import ParametrosEquivocados, CuentasNoCuadran


class SalaReuniones(ServicioBase):
    def __init__(self, nombre, descripcion, precio, limite=5, aforo=10):
        super().__init__(nombre, descripcion, precio, limite)
        self.aforo = aforo
    
    def tipo(self):
        return "sala"
    
    def validar_datos(self, **datos):
        personas = datos.get('personas')
        if personas is not None:
            try:
                personas = int(personas)
                if personas <= 0:
                    raise ParametrosEquivocados("personas debe ser mayor a 0")
                if personas > self.aforo:
                    raise ParametrosEquivocados(f"maximo {self.aforo} personas")
            except:
                raise ParametrosEquivocados("personas debe ser un numero")
        
        extras = datos.get('extras')
        if extras is not None and not isinstance(extras, list):
            raise ParametrosEquivocados("extras debe ser una lista")
        return True
    
    def calcular_precio(self, horas, **datos):
        self.validar_datos(**datos)
        if horas <= 0:
            raise CuentasNoCuadran(f"horas invalidas: {horas}")
        
        total = self.precio_base * horas
        
        descuento = datos.get('descuento', 0.0)
        if descuento < 0 or descuento > 100:
            raise CuentasNoCuadran("descuento invalido")
        total = total * (1 - descuento / 100)
        
        impuesto = datos.get('impuesto', 0.0)
        if impuesto < 0:
            raise CuentasNoCuadran("impuesto invalido")
        total = total * (1 + impuesto / 100)
        
        extras = datos.get('extras', [])
        total += len(extras) * 10.0
        
        return round(total, 2)
    
    def info(self):
        return f"Sala: {self.nombre}\nAforo: {self.aforo}\nPrecio: ${self.precio_base}/h"


class EquipoTecnologico(ServicioBase):
    def __init__(self, nombre, descripcion, precio, limite=20, tipo="computadora"):
        super().__init__(nombre, descripcion, precio, limite)
        self.tipo_equipo = tipo
        self.stock = 10
    
    def tipo(self):
        return "equipo"
    
    def validar_datos(self, **datos):
        cantidad = datos.get('cantidad')
        if cantidad is not None:
            try:
                cantidad = int(cantidad)
                if cantidad <= 0:
                    raise ParametrosEquivocados("cantidad debe ser mayor a 0")
                if cantidad > self.stock:
                    raise ParametrosEquivocados(f"solo hay {self.stock} disponibles")
            except:
                raise ParametrosEquivocados("cantidad debe ser un numero")
        
        software = datos.get('software_especial')
        if software is not None and not isinstance(software, bool):
            raise ParametrosEquivocados("software_especial debe ser True/False")
        return True
    
    def calcular_precio(self, horas, **datos):
        self.validar_datos(**datos)
        if horas <= 0:
            raise CuentasNoCuadran(f"horas invalidas: {horas}")
        
        cantidad = datos.get('cantidad', 1)
        if cantidad <= 0:
            cantidad = 1
        
        total = self.precio_base * horas * cantidad
        
        if cantidad >= 5:
            descuento = datos.get('descuento', 0.0)
            if descuento < 0 or descuento > 100:
                raise CuentasNoCuadran("descuento invalido")
            total = total * (1 - descuento / 100)
        
        software = datos.get('software_especial', False)
        if software:
            total += 25.0 * cantidad
        
        impuesto = datos.get('impuesto', 0.0)
        if impuesto < 0:
            raise CuentasNoCuadran("impuesto invalido")
        total = total * (1 + impuesto / 100)
        
        return round(total, 2)
    
    def info(self):
        return f"Equipo: {self.nombre}\nTipo: {self.tipo_equipo}\nPrecio: ${self.precio_base}/h/unidad"


class AsesoriaEspecializada(ServicioBase):
    def __init__(self, nombre, descripcion, precio, limite=3, nivel="senior"):
        super().__init__(nombre, descripcion, precio, limite)
        self.nivel = nivel
    
    def tipo(self):
        return "asesoria"
    
    def validar_datos(self, **datos):
        nivel = datos.get('nivel')
        if nivel is not None:
            if nivel not in ['junior', 'senior', 'expert']:
                raise ParametrosEquivocados("nivel debe ser junior/senior/expert")
        
        urgente = datos.get('urgente')
        if urgente is not None and not isinstance(urgente, bool):
            raise ParametrosEquivocados("urgente debe ser True/False")
        return True
    
    def calcular_precio(self, horas, **datos):
        self.validar_datos(**datos)
        if horas <= 0:
            raise CuentasNoCuadran(f"horas invalidas: {horas}")
        
        factores = {'junior': 1.0, 'senior': 1.5, 'expert': 2.0}
        nivel = datos.get('nivel', self.nivel)
        factor = factores.get(nivel, 1.0)
        
        total = self.precio_base * horas * factor
        
        urgente = datos.get('urgente', False)
        if urgente:
            total *= 1.3
        
        descuento = datos.get('descuento', 0.0)
        if descuento < 0 or descuento > 100:
            raise CuentasNoCuadran("descuento invalido")
        total = total * (1 - descuento / 100)
        
        impuesto = datos.get('impuesto', 0.0)
        if impuesto < 0:
            raise CuentasNoCuadran("impuesto invalido")
        total = total * (1 + impuesto / 100)
        
        return round(total, 2)
    
    def info(self):
        return f"Asesoria: {self.nombre}\nNivel: {self.nivel}\nPrecio: ${self.precio_base}/h"