from datetime import datetime
import csv
import os
from cliente import Cliente
from turno import Turno 

class GestorTurnos:
    ARCHIVO_CSV = 'turnos.csv'

    def __init__(self):
        self.turnos = {}
        self._cargar_datos()#con self. llamamos al metodo _cargar_datos

    def _cargar_datos(self):
        if not os.path.exists(self.ARCHIVO_CSV): 
            return
        
        try:#con try hacemos manejos de excepciones y errores
            with open(self.ARCHIVO_CSV, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    cliente = Cliente(nombre=row['cliente_nombre'], telefono=row['cliente_telefono'])
                    turno = Turno(cliente=cliente, fecha_hora_str=row['fecha_hora'], 
                                  servicio=row['servicio'], id=row['id'])
                    self.turnos[turno.id] = turno
            print(f"Hay {len(self.turnos)} turnos cargados.") 
        except Exception as e:
            print(f"Error: El archivo CSV tiene un formato incorrecto. {e}")
            self.turnos = {}

    def _guardar_datos(self):
        if not self.turnos and os.path.exists(self.ARCHIVO_CSV):
            os.remove(self.ARCHIVO_CSV)
            print("Lista está vacía.")#si la lista está vacia en la opcion 5 devuelve este mensaje
            return

        fieldnames = ['id', 'cliente_nombre', 'cliente_telefono', 'fecha_hora', 'servicio']#si hay datos en el csv, en la opción 4
        try:                                                                               #lista los archivos en este formato
            with open(self.ARCHIVO_CSV, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for turno in self.turnos.values():
                    writer.writerow(turno.to_dict())
            print("Datos guardados en CSV.")#si hay datos seleccionando opción 5 deviuelve este mensaje
        except Exception as e:
            print(f"Error: No se pudo escribir en el CSV. {e}")

    def buscar_id_por_datos(self, nombre_cliente, fecha_hora_str):
        try:#con try hacemos manejos de excepciones y errores
            fecha_hora_buscada = datetime.strptime(fecha_hora_str, '%d/%m/%Y %H:%M')
        except ValueError:
            return None

        turnos_list = list(self.turnos.values())
        i = 0
        while i < len(turnos_list):
            turno = turnos_list[i]
            if (turno.cliente.nombre.lower() == nombre_cliente.lower() and 
                turno.fecha_hora == fecha_hora_buscada):
                return turno.id
            i += 1
        return None
    
    def registrar_turno(self, cliente, fecha_hora_str, servicio):
        try:#con try hacemos manejos de excepciones y errores
            nuevo_turno = Turno(cliente, fecha_hora_str, servicio)
        except ValueError:
            print("Error: Verifique el formato de fecha y hora.")#en la opcion 2 si esta mal escrita la
            return False                                         #fecha y hora devuelve este mensaje

        turnos_list = list(self.turnos.values())#busca y lista todos los turnos para comparar
        i = 0
        while i < len(turnos_list):# el contador para iterar mientras el indice sea menor al numero de turnos
            if turnos_list[i].fecha_hora == nuevo_turno.fecha_hora:# si el horario esta ocupado
                print("Error: Horario ocupado.")#evita superposicion y devuelve el mensaje
                return False
            i += 1#incremente en 1 cada ciclo
        #mientras no haya colision, ejecuta lo siguiente
        self.turnos[nuevo_turno.id] = nuevo_turno#guarda el nuevo turno en self.turnos
        self._guardar_datos()#con este metodo se le da persistencia a los datos
        print(f"Se creó el turno para {cliente.nombre}.")
        return True

    def listar_turnos(self):
        if not self.turnos:
            print("No hay turnos registrados.")#en la opción 3 cuado se pide listar los turnos,
            return                             #si no hay ninguno devuelve este mensaje

        print("\nLista de turnos cargados")
        turnos_ordenados = sorted(self.turnos.values(), key=lambda t: t.fecha_hora)#lista los turnos cronologicamente
        for i, turno in enumerate(turnos_ordenados, 1):
            print(f"({i}) ID: {turno.id[:8]} | Cliente: {turno.cliente.nombre} | Hora: {turno.fecha_hora.strftime('%H:%M')}")
        print("\n")

    def modificar_o_cancelar(self, id_turno, operacion, nueva_fecha_hora_str=None):
        if id_turno not in self.turnos:#si no hay turnos
            print("Error: Turno no encontrado.")#devuelve este mensaje
            return

        turno = self.turnos[id_turno]

        if operacion == 'm':#en la opción 4, si presionamos m hace lo siguiente
            try:#con try hacemos manejos de excepciones y errores
                nueva_fecha_hora = datetime.strptime(nueva_fecha_hora_str, '%d/%m/%Y %H:%M')
            except ValueError:
                print("Error: Formato de fecha y hora invalido.")
                return
            
            ######superposicion de turnos######
            turnos_list = list(self.turnos.values())
            i = 0
            while i < len(turnos_list): #Compara dentro de la memoria con los turnos cargados
                t = turnos_list[i]
                if t.id != id_turno and t.fecha_hora == nueva_fecha_hora:
                    print("ERROR: Horario ya ocupado.")# si ya existe el turno devuelve este mensaje
                    return
                i += 1

            turno.fecha_hora = nueva_fecha_hora
            self._guardar_datos()
            print(f"Se modificó el turno con la fecha {nueva_fecha_hora_str}.")
        
        elif operacion == 'c':#presionando c, cancela el turno
            del self.turnos[id_turno]
            self._guardar_datos()
            print("Turno cancelado.")