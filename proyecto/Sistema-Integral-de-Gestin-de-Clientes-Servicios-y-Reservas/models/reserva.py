from datetime import datetime, timedelta
from exceptions.excepciones import EstadoReservaRaro, FechaEquivocada

contador_reservas = 0

class Reserva:
    def __init__(self, cliente, servicio, fecha_inicio, duracion, **datos):
        global contador_reservas
        contador_reservas += 1
        self.numero = contador_reservas
        
        self.cliente = cliente
        self.servicio = servicio
        self.fecha_inicio = fecha_inicio
        self.duracion = duracion
        self.datos_extra = datos
        
        self._validar_fechas()
        
        self._estado = 'pendiente'
        self.fecha_creacion = datetime.now()
        self.fecha_confirmacion = None
        self.fecha_cancelacion = None
        self.fecha_terminado = None
        self._costo = None
    
    def _validar_fechas(self):
        ahora = datetime.now()
        if self.fecha_inicio < ahora - timedelta(minutes=5):
            raise FechaEquivocada("la fecha debe ser futura")
        if self.duracion <= 0:
            raise FechaEquivocada("la duracion debe ser mayor a 0")
        if self.duracion > 24:
            raise FechaEquivocada("la duracion maxima es 24 horas")
    
    @property
    def estado(self):
        return self._estado
    
    @property
    def costo(self):
        return self._costo
    
    def confirmar(self):
        if self._estado != 'pendiente':
            raise EstadoReservaRaro(self._estado, 'confirmada')
        
        try:
            self.servicio.reservar()
            self._costo = self.servicio.calcular_precio(
                self.duracion,
                **self.datos_extra
            )
            self._estado = 'confirmada'
            self.fecha_confirmacion = datetime.now()
            return self._costo
        except Exception as e:
            raise EstadoReservaRaro('pendiente', 'confirmada') from e
    
    def cancelar(self):
        if self._estado not in ['pendiente', 'confirmada']:
            raise EstadoReservaRaro(self._estado, 'cancelada')
        
        if self._estado == 'confirmada':
            self.servicio.liberar()
        
        self._estado = 'cancelada'
        self.fecha_cancelacion = datetime.now()
    
    def terminar(self):
        if self._estado != 'confirmada':
            raise EstadoReservaRaro(self._estado, 'terminada')
        
        self._estado = 'terminada'
        self.fecha_terminado = datetime.now()
        self.servicio.liberar()
    
    def costo_con_descuento_extra(self, descuento_extra=0.0):
        if self._costo is None:
            raise ValueError("la reserva debe estar confirmada")
        if descuento_extra < 0 or descuento_extra > 100:
            raise ValueError("descuento invalido")
        return self._costo * (1 - descuento_extra / 100)
    
    def __str__(self):
        return (f"Reserva #{self.numero} | {self.cliente.nombre} → {self.servicio.nombre}\n"
                f"  Estado: {self._estado.upper()}\n"
                f"  Fecha: {self.fecha_inicio.strftime('%d/%m/%Y %H:%M')}\n"
                f"  Duracion: {self.duracion}h\n"
                f"  Costo: ${self._costo if self._costo else 'No calculado'}")