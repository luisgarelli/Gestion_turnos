from datetime import datetime#se usa para trabajar con fechas y poder manipularlas
import uuid#le da un id a cada turno sin que se repitan
from cliente import Cliente #asocia turno con cliente

class Turno:
    def __init__(self, cliente, fecha_hora_str, servicio, id=None):
        self.id = id if id else str(uuid.uuid4())
        self.cliente = cliente
        self.servicio = servicio
        
        self.fecha_hora = datetime.strptime(fecha_hora_str, '%d/%m/%Y %H:%M') 

    def __str__(self):#funcion para darle formato a la fecha
        fecha_formato = self.fecha_hora.strftime('%d/%m/%Y %H:%M')
        return (f"ID: {self.id[:8]}, Fecha: {fecha_formato}, "
                f"Servicio: {self.servicio}, Cliente: {self.cliente.nombre}")

    def to_dict(self):#to_dict hace persistentes a los datos
        return {
            'id': self.id,
            'cliente_nombre': self.cliente.nombre,
            'cliente_telefono': self.cliente.telefono,
            'fecha_hora': self.fecha_hora.strftime('%d/%m/%Y %H:%M'),
            'servicio': self.servicio
        }