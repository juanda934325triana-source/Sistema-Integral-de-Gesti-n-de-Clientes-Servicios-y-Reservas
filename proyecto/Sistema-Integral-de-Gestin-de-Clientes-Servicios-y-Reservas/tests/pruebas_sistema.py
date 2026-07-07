from datetime import datetime, timedelta
from models.gestor import SoftwareFJ
from exceptions.excepciones import *

def ejecutar_pruebas():
    print("="*60)
    print("EJECUTANDO PRUEBAS DEL SISTEMA")
    print("="*60)
    
    sistema = SoftwareFJ()
    
    # Prueba 1: Registrar cliente válido
    try:
        c1 = sistema.registrar_cliente("Juan Perez", "juan@email.com", "3001234567", "premium")
        print("✅ Cliente registrado correctamente")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Prueba 2: Cliente duplicado
    try:
        sistema.registrar_cliente("Pedro Gomez", "juan@email.com", "3007654321", "regular")
        print("❌ Deberia haber fallado")
    except ClienteYaExiste:
        print("✅ Cliente duplicado detectado")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    
    # Prueba 3: Datos inválidos
    try:
        sistema.registrar_cliente("A", "email-invalido", "123", "regular")
        print("❌ Deberia haber fallado")
    except DatosClienteMalos:
        print("✅ Datos invalidos detectados")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    
    # Prueba 4: Crear servicio sala
    try:
        sala = sistema.crear_sala("Sala Ejecutiva", "Sala para juntas", 60, 15)
        print(f"✅ Sala creada (ID: {sala.id})")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Prueba 5: Crear servicio equipo
    try:
        equipo = sistema.crear_equipo("Laptop Dell", "Laptop para alquiler", 25, "laptop")
        print(f"✅ Equipo creado (ID: {equipo.id})")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Prueba 6: Crear servicio asesoria
    try:
        asesoria = sistema.crear_asesoria("Consultoria Python", "Asesoria en Python", 80, "senior")
        print(f"✅ Asesoria creada (ID: {asesoria.id})")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Prueba 7: Crear reserva
    try:
        fecha = datetime.now() + timedelta(days=1)
        reserva = sistema.crear_reserva(c1.id, sala.id, fecha, 2, personas=5)
        print(f"✅ Reserva creada (ID: {reserva.numero})")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Prueba 8: Confirmar reserva
    try:
        costo = sistema.confirmar_reserva(reserva.numero)
        print(f"✅ Reserva confirmada. Costo: ${costo:.2f}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Prueba 9: Cancelar reserva
    try:
        sistema.cancelar_reserva(reserva.numero)
        print("✅ Reserva cancelada")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Prueba 10: Estadisticas
    try:
        stats = sistema.estadisticas()
        print("✅ Estadisticas obtenidas")
        print(f"   Clientes: {stats['total_clientes']}")
        print(f"   Servicios: {stats['total_servicios']}")
        print(f"   Reservas: {stats['total_reservas']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("="*60)
    print("PRUEBAS COMPLETADAS")
    print("="*60)

if __name__ == "__main__":
    ejecutar_pruebas()