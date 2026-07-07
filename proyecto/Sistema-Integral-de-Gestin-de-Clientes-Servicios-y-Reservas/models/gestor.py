from datetime import datetime
from models.cliente import Cliente
from models.servicios_concretos import SalaReuniones, EquipoTecnologico, AsesoriaEspecializada
from models.reserva import Reserva
from exceptions.excepciones import ClienteNoExiste, ClienteYaExiste, ServicioNoExiste, ReservaNoExiste
from utils.logger import get_logger


class SoftwareFJ:
    def __init__(self):
        self.clientes = {}
        self.servicios = {}
        self.reservas = []
        self.log = get_logger()
        self.log.info("sistema iniciado")
    
    def registrar_cliente(self, nombre, email, telefono, tipo="regular"):
        for c in self.clientes.values():
            if c.email == email.lower():
                raise ClienteYaExiste(email)
        
        cliente = Cliente(nombre, email, telefono, tipo)
        self.clientes[cliente.id] = cliente
        self.log.info(f"cliente registrado: {cliente.nombre}")
        return cliente
    
    def buscar_cliente(self, id_cliente):
        if id_cliente not in self.clientes:
            raise ClienteNoExiste(id_cliente)
        return self.clientes[id_cliente]
    
    def listar_clientes(self):
        return list(self.clientes.values())
    
    def crear_sala(self, nombre, descripcion, precio, aforo=10):
        servicio = SalaReuniones(nombre, descripcion, precio, aforo=aforo)
        self.servicios[servicio.id] = servicio
        self.log.info(f"sala creada: {nombre}")
        return servicio
    
    def crear_equipo(self, nombre, descripcion, precio, tipo="computadora"):
        servicio = EquipoTecnologico(nombre, descripcion, precio, tipo=tipo)
        self.servicios[servicio.id] = servicio
        self.log.info(f"equipo creado: {nombre}")
        return servicio
    
    def crear_asesoria(self, nombre, descripcion, precio, nivel="senior"):
        servicio = AsesoriaEspecializada(nombre, descripcion, precio, nivel=nivel)
        self.servicios[servicio.id] = servicio
        self.log.info(f"asesoria creada: {nombre}")
        return servicio
    
    def buscar_servicio(self, id_servicio):
        if id_servicio not in self.servicios:
            raise ServicioNoExiste(id_servicio)
        return self.servicios[id_servicio]
    
    def listar_servicios(self):
        return list(self.servicios.values())
    
    def servicios_disponibles(self):
        return [s for s in self.servicios.values() if s.disponible]
    
    def crear_reserva(self, id_cliente, id_servicio, fecha_inicio, horas, **datos):
        cliente = self.buscar_cliente(id_cliente)
        servicio = self.buscar_servicio(id_servicio)
        
        reserva = Reserva(cliente, servicio, fecha_inicio, horas, **datos)
        self.reservas.append(reserva)
        self.log.info(f"reserva creada: #{reserva.numero}")
        return reserva
    
    def confirmar_reserva(self, num_reserva):
        for r in self.reservas:
            if r.numero == num_reserva:
                costo = r.confirmar()
                self.log.info(f"reserva {num_reserva} confirmada, costo: ${costo}")
                return costo
        
        raise ReservaNoExiste(num_reserva)
    
    def cancelar_reserva(self, num_reserva):
        for r in self.reservas:
            if r.numero == num_reserva:
                r.cancelar()
                self.log.info(f"reserva {num_reserva} cancelada")
                return
        
        raise ReservaNoExiste(num_reserva)
    
    def terminar_reserva(self, num_reserva):
        for r in self.reservas:
            if r.numero == num_reserva:
                r.terminar()
                self.log.info(f"reserva {num_reserva} terminada")
                return
        
        raise ReservaNoExiste(num_reserva)
    
    def listar_reservas(self):
        return self.reservas.copy()
    
    def reservas_activas(self):
        return [r for r in self.reservas if r.estado in ['pendiente', 'confirmada']]
    
    def estadisticas(self):
        return {
            'total_clientes': len(self.clientes),
            'total_servicios': len(self.servicios),
            'total_reservas': len(self.reservas),
            'reservas_activas': len(self.reservas_activas())
        }