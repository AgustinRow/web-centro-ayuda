from app.view.reservaView import ReservaView

class ReservaFactory():
    idCentro = ""
    nombre = ""
    apellido = ""
    email_donante = ""
    telefono_donante = ""
    fecha = ""
    horaInicio = ""
    horaFin = ""    

    def __init__(self, idCentro, nombre, apellido, email_donante, telefono_donante, fecha, horaInicio, horaFin):
        self.idCentro = idCentro
        self.nombre = nombre
        self.apellido = apellido
        self.email_donante = email_donante
        self.telefono_donante = telefono_donante
        self.fecha = fecha
        self.horaInicio = horaInicio
        self.horaFin = horaFin
    
    def serializar(self):
        reservaView = ReservaView()
        res = reservaView.dump(self)

        return res
