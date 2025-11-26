from gestor import GestorTurnos
from cliente import Cliente 

def menu_principal():
    gestor = GestorTurnos() 

    while True:
        print("\n")
        print("MENU PRINCIPAL") 
        print("\n")
        print("1. Registrar nuevo cliente")
        print("2. Solicitar turno")
        print("3. Listar turnos existentes")
        print("4. Modificar o cancelar turno")
        print("5. Guardar datos en CSV / Cargar desde dict")
        print("6. Salir")
        print("\n")
        
        opcion = input("Opcion: ").strip()

        if opcion == '1':
            print("\nREGISTRAR CLIENTE")
            print(f"{input('Nombre: ').strip()} ha sido registrado.")
            
        else:
            if opcion == '2':
                print("\nSOLICITAR TURNO")
                gestor.registrar_turno(Cliente(input("Nombre: ").strip(), input("Telefono: ").strip()), 
                                       input("Fecha (dd/mm/aaaa): ").strip() + " " + input("Hora (hh:mm): ").strip(),
                                       input("Servicio: ").strip())

            else:
                if opcion == '3':
                    gestor.listar_turnos()#busca en el archivo gestor.py la función listar_turnos
                                          # y busca datos para listar.
                else:
                    if opcion == '4':
                        print("\nBUSCAR TURNO")
                        
                        nom = input("Nombre cliente: ").strip()
                        fec = input("Fecha original (dd/mm/aaaa): ").strip()
                        hor = input("Hora original (hh:mm): ").strip()
                        fecha_hora_original_str = f"{fec} {hor}"#contiene el turno guardado a modificar o cancelar
                        
                        turno_id = gestor.buscar_id_por_datos(nom, fecha_hora_original_str)#busca el turno por nombre, fecha y hora
                        
                        if not turno_id:
                            print("Turno no encontrado")
                            continue #me lleva al menú nuevamente

                        accion = input("¿Presionar ¨m¨ para modifica y ¨c¨ para cancelar?: ").lower().strip()
                        
                        if accion == 'm':
                            print("\nMODIFICAR")
                            gestor.modificar_o_cancelar(turno_id, 'm', 
                                input("Nueva fecha (dd/mm/aaaa): ").strip() + " " + input("Nueva hora (hh:mm): ").strip())
                        
                        elif accion == 'c':
                            gestor.modificar_o_cancelar(turno_id, 'c')
                        
                        else:
                            print("Accion no valida.")#si no seleccionamos m o c, muestra este mensaje

                    else:
                        if opcion == '5':
                            gestor._guardar_datos()
                            gestor._cargar_datos()
                            print("Datos guardados")

                        else:
                            if opcion == '6':
                                print("Saliendo del programa.")
                                break

                            else:
                                print("Opcion no valida.")#esta excepcion se usa cuando se escribe 0 o numero >=7

if __name__ == "__main__":
    menu_principal()