class Cliente:
    #atributos del objeto
    def __init__(self, nombre, telefono):
        self.nombre = nombre
        self.telefono = telefono

    def __str__(self):
        return f"Cliente: {self.nombre}, Tel.: {self.telefono}"

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'telefono': self.telefono
        }