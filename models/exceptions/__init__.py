class ErrorSistema(Exception):
    def __init__(self, msg, cod=999):
        self.cod = cod
        self.msg = msg
        super().__init__(f"{cod} - {msg}")


class ErrorCliente(ErrorSistema):
    pass


class ClienteNoExiste(ErrorCliente):
    def __init__(self, identificador):
        self.ident = identificador
        try:
            int(identificador)
            super().__init__(f"Cliente con ID {identificador} no existe", 101)
        except:
            super().__init__(f"Cliente con email/nombre '{identificador}' no existe", 101)


class ClienteYaExiste(ErrorCliente):
    def __init__(self, email):
        self.email = email
        if "gmail" in email or "hotmail" in email:
            super().__init__(f"Ese email {email} ya esta registrado, usa otro", 102)
        else:
            super().__init__(f"Email {email} ya registrado", 102)


class DatosClienteMalos(ErrorCliente):
    def __init__(self, campo, valor):
        self.campo = campo
        self.valor = valor
        if campo == "nombre":
            super().__init__(f"Nombre invalido: {valor} - minimo 3 letras", 103)
        elif campo == "email":
            super().__init__(f"Email invalido: {valor} - formato incorrecto", 103)
        elif campo == "telefono":
            super().__init__(f"Telefono invalido: {valor} - solo numeros", 103)
        else:
            super().__init__(f"{campo} invalido: {valor}", 103)


class ErrorServicio(ErrorSistema):
    pass


class ServicioNoExiste(ErrorServicio):
    def __init__(self, id_servicio):
        self.id = id_servicio
        if id_servicio <= 0:
            super().__init__(f"ID invalido: {id_servicio}", 200)
        else:
            super().__init__(f"Servicio {id_servicio} no existe", 201)


class ServicioOcupado(ErrorServicio):
    def __init__(self, nombre):
        self.nombre = nombre
        super().__init__(f"{nombre} no disponible en este momento", 202)


class ParametrosEquivocados(ErrorServicio):
    def __init__(self, detalle):
        self.detalle = detalle
        if len(detalle) > 50:
            detalle = detalle[:47] + "..."
        super().__init__(f"Datos invalidos: {detalle}", 203)


class CupoCompleto(ErrorServicio):
    def __init__(self, servicio, capacidad, solicitado):
        self.servicio = servicio
        self.capacidad = capacidad
        self.solicitado = solicitado
        if solicitado < 1:
            super().__init__(f"Pidieron {solicitado}? minimo 1", 205)
        elif solicitado > capacidad:
            super().__init__(f"{servicio} solo aguanta {capacidad}, pidieron {solicitado}", 204)
        else:
            super().__init__(f"{servicio} maximo {capacidad}, pidieron {solicitado}", 204)


class ErrorReserva(ErrorSistema):
    pass


class ReservaNoExiste(ErrorReserva):
    def __init__(self, num):
        self.num = num
        if num < 100:
            super().__init__(f"Reserva #{num} no existe, revisa el ID", 301)
        else:
            super().__init__(f"Reserva #{num} no existe", 301)


class EstadoReservaRaro(ErrorReserva):
    def __init__(self, actual, deseado):
        self.actual = actual
        self.deseado = deseado
        if actual == "cancelada" and deseado == "confirmada":
            super().__init__(f"Ya cancelaste esta reserva, no la puedes confirmar", 302)
        elif actual == "terminada" and deseado == "cancelada":
            super().__init__(f"La reserva ya termino, no se puede cancelar", 302)
        elif actual == "pendiente" and deseado == "terminada":
            super().__init__(f"Primero confirma la reserva antes de terminarla", 302)
        else:
            super().__init__(f"No se puede pasar de {actual} a {deseado}", 302)


class FechaEquivocada(ErrorReserva):
    def __init__(self, problema):
        self.problema = problema
        if "futura" in problema:
            super().__init__(f"Elige una fecha futura", 303)
        elif "duracion" in problema:
            super().__init__(f"Duracion invalida", 303)
        else:
            super().__init__(f"Fecha invalida: {problema}", 303)


class ErrorPago(ErrorSistema):
    pass


class CuentasNoCuadran(ErrorPago):
    def __init__(self, detalle):
        self.detalle = detalle
        if "descuento" in detalle.lower():
            super().__init__(f"Descuento invalido", 400)
        elif "impuesto" in detalle.lower():
            super().__init__(f"Impuesto invalido", 401)
        elif "horas" in detalle.lower():
            super().__init__(f"Horas invalidas", 402)
        else:
            super().__init__(f"Error en calculo: {detalle}", 404)
