from app.db_sqlalchemy import db_sqlalchemy
from datetime import datetime,date,time,timedelta
db = db_sqlalchemy
metadata = db.MetaData()


class Turno(db.Model):
    __tablename__ = 'centros_turnos'
    id = db.Column(db.Integer, primary_key=True)
    email_contacto = db.Column(db.String(255),nullable=True)
    nombre = db.Column(db.String(255), nullable=True)
    apellido = db.Column(db.String(255), nullable=True)
    telefono_contacto = db.Column(db.String(255),nullable=True)
    fecha = db.Column(db.Date(), nullable=True)
    hora_inicio = db.Column(db.Time(), nullable=True)
    hora_fin = db.Column(db.Time(), nullable=True)
    enabled = db.Column(db.Integer,nullable=False)
    

    def __init__(self, email, fecha, hora, telefono, nombre, apellido):
        self.email_contacto = email
        self.fecha = fecha
        self.hora_inicio = hora
        minutes = timedelta(minutes=30)
        self.hora_fin = self.hora_inicio + minutes
        self.telefono_contacto=telefono
        self.enabled=1
        self.nombre = nombre
        self.apellido = apellido

    def save(self):
        db.session.add(self)
        db.session.commit()
        return True

    def __repr__(self):
        return '<Turno {0} {1} {2} {3} {4}>'.format(self.email_contacto,
                                                self.fecha,
                                                self.hora_inicio,
                                                self.hora_fin,
                                                self.telefono_contacto)

    @staticmethod
    def all():
        return Turno.query.filter_by(enabled=1)

    def actualizar(self):
        db.session.commit()
        return True


    def filtarPorMail(email):
        consulta = db.session.query(Turno).filter_by(email_contacto=email,enabled=1)
        return consulta

    def todosComoQuery():
        return Turno.query.filter_by()

    def eliminarPorId(idTurno):
        turno = Turno.buscarPorId(idTurno)
        turno.enabled=0
        turno.actualizar()
        return True
    
    def buscarPorId(idTurno):
        return Turno.query.filter_by(id=idTurno,enabled=1).first()
