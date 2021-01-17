from app.view.turnoView import TurnoView

class TurnoFactory():
        idCentro=""
        fecha=""
        horaInicio=""
        horaFin=""    
        
        def __init__(self, idCentro, fecha, horaInicio, horaFin):
            self.idCentro = idCentro
            self.fecha = fecha
            self.horaInicio = horaInicio
            self.horaFin = horaFin

        def serializar(self):
            turnoView = TurnoView()
            res = turnoView.dump(self)

            return res
