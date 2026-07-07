from datetime import datetime
from models.gestor import SoftwareFJ
from utils.logger import get_logger
from exceptions.excepciones import *


def mostrar_menu():
    print("\n" + "="*50)
    print("SOFTWARE FJ - GESTION")
    print("="*50)
    print("1. Registrar cliente")
    print("2. Ver clientes")
    print("3. Crear servicio")
    print("4. Ver servicios")
    print("5. Crear reserva")
    print("6. Confirmar reserva")
    print("7. Cancelar reserva")
    print("8. Terminar reserva")
    print("9. Ver reservas")
    print("10. Ver estadisticas")
    print("0. Salir")
    print("="*50)


def main():
    sistema = SoftwareFJ()
    log = get_logger()
    
    # Datos de ejemplo
    try:
        sistema.registrar_cliente("Ana Garcia", "ana@email.com", "3001234567", "premium")
        sistema.registrar_cliente("Carlos Lopez", "carlos@email.com", "3007654321", "regular")
        sistema.crear_sala("Sala A", "Sala de reuniones", 50, 10)
        sistema.crear_equipo("HP Laptop", "Laptop HP", 20, "laptop")
        sistema.crear_asesoria("Python", "Asesoria en Python", 80, "senior")
        print("✅ Datos de ejemplo cargados")
    except:
        pass
    
    while True:
        try:
            mostrar_menu()
            opcion = input("Opcion: ").strip()
            
            if opcion == "0":
                print("\n¡Hasta luego!")
                log.info("sistema cerrado")
                break
            
            elif opcion == "1":
                try:
                    nombre = input("Nombre: ")
                    email = input("Email: ")
                    telefono = input("Telefono: ")
                    tipo = input("Tipo (regular/premium/empresarial): ") or "regular"
                    
                    cliente = sistema.registrar_cliente(nombre, email, telefono, tipo)
                    print(f"✅ Cliente registrado con ID: {cliente.id}")
                except (DatosClienteMalos, ClienteYaExiste) as e:
                    print(f"❌ Error: {e}")
            
            elif opcion == "2":
                clientes = sistema.listar_clientes()
                if clientes:
                    print("\n📋 CLIENTES:")
                    for c in clientes:
                        print(f"  {c}")
                else:
                    print("No hay clientes registrados")
            
            elif opcion == "3":
                print("\nTipos: sala, equipo, asesoria")
                tipo = input("Tipo: ").lower()
                nombre = input("Nombre: ")
                descripcion = input("Descripcion: ")
                try:
                    precio = float(input("Precio por hora: "))
                except:
                    print("❌ Precio invalido")
                    continue
                
                try:
                    if tipo == "sala":
                        aforo = int(input("Aforo: ") or "10")
                        servicio = sistema.crear_sala(nombre, descripcion, precio, aforo)
                    elif tipo == "equipo":
                        tipo_eq = input("Tipo de equipo: ") or "computadora"
                        servicio = sistema.crear_equipo(nombre, descripcion, precio, tipo_eq)
                    elif tipo == "asesoria":
                        nivel = input("Nivel (junior/senior/expert): ") or "senior"
                        servicio = sistema.crear_asesoria(nombre, descripcion, precio, nivel)
                    else:
                        print("❌ Tipo invalido")
                        continue
                    
                    print(f"✅ Servicio creado con ID: {servicio.id}")
                except Exception as e:
                    print(f"❌ Error: {e}")
            
            elif opcion == "4":
                servicios = sistema.listar_servicios()
                if servicios:
                    print("\n📋 SERVICIOS:")
                    for s in servicios:
                        print(f"  {s}")
                else:
                    print("No hay servicios")
            
            elif opcion == "5":
                try:
                    id_cliente = int(input("ID del cliente: "))
                    id_servicio = int(input("ID del servicio: "))
                    
                    fecha_str = input("Fecha (YYYY-MM-DD HH:MM): ")
                    fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")
                    horas = float(input("Horas: "))
                    
                    reserva = sistema.crear_reserva(id_cliente, id_servicio, fecha, horas)
                    print(f"✅ Reserva creada con ID: {reserva.numero} (pendiente)")
                except (ValueError, ClienteNoExiste, ServicioNoExiste, FechaEquivocada) as e:
                    print(f"❌ Error: {e}")
            
            elif opcion == "6":
                try:
                    num = int(input("ID de la reserva: "))
                    costo = sistema.confirmar_reserva(num)
                    print(f"✅ Reserva confirmada. Costo: ${costo:.2f}")
                except (ValueError, ReservaNoExiste, EstadoReservaRaro, ServicioOcupado) as e:
                    print(f"❌ Error: {e}")
            
            elif opcion == "7":
                try:
                    num = int(input("ID de la reserva: "))
                    sistema.cancelar_reserva(num)
                    print("✅ Reserva cancelada")
                except (ValueError, ReservaNoExiste, EstadoReservaRaro) as e:
                    print(f"❌ Error: {e}")
            
            elif opcion == "8":
                try:
                    num = int(input("ID de la reserva: "))
                    sistema.terminar_reserva(num)
                    print("✅ Reserva terminada")
                except (ValueError, ReservaNoExiste, EstadoReservaRaro) as e:
                    print(f"❌ Error: {e}")
            
            elif opcion == "9":
                reservas = sistema.listar_reservas()
                if reservas:
                    print("\n📋 RESERVAS:")
                    for r in reservas:
                        print(f"  {r}")
                else:
                    print("No hay reservas")
            
            elif opcion == "10":
                stats = sistema.estadisticas()
                print("\n📊 ESTADISTICAS:")
                print(f"  Clientes: {stats['total_clientes']}")
                print(f"  Servicios: {stats['total_servicios']}")
                print(f"  Reservas: {stats['total_reservas']}")
                print(f"  Reservas activas: {stats['reservas_activas']}")
            
            else:
                print("❌ Opcion no valida")
        
        except KeyboardInterrupt:
            print("\n¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            log.exception(f"Error: {e}")


if __name__ == "__main__":
    main()