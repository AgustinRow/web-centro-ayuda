from app.db_sqlalchemy import db_sqlalchemy
from datetime import datetime

from app.models.turno import Turno
db = db_sqlalchemy
metadata = db.MetaData()


class Centro(db.Model):
    __tablename__ = 'centros_centros'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    direccion = db.Column(db.String(255))
    telefono = db.Column(db.String(255))
    tipo = db.Column(db.String(255))
    municipio = db.Column(db.String(255))
    latitud = db.Column(db.Float, nullable=True)
    longitud = db.Column(db.Float, nullable=True)
    horario_apertura = db.Column(db.Time(), nullable=True)
    horario_cierra = db.Column(db.Time(), nullable=True)
    web = db.Column(db.String(255))
    email = db.Column(db.String(255))
    enabled = db.Column(db.Integer)
    nombre_archivo_hasheado = db.Column(db.String)
    nombre_archivo = db.Column(db.String)
    disponible = db.Column(db.Integer)  # 0 pediente, 1 aceptado, 2 rechazado
    estado = db.Column(db.Integer)

    association_table = db.Table('centros_centros_tiene_turnos', metadata,
                                 db.Column('centro_id', db.Integer,
                                           db.ForeignKey(id)),
                                 db.Column('turno_id', db.Integer, db.ForeignKey(Turno.id)))

    turnos = db.relationship("Turno",
                             secondary=association_table,
                             )

    def __init__(self, nombre, direccion, tipo, telefono, municipio, web, nombre_archivo_hasheado, estado, latitud, longitud, horario_apertura, horario_cierre, email, disponible, nombre_archivo):
        self.nombre = nombre
        self.direccion = direccion
        self.tipo = tipo
        self.latitud = latitud
        self.longitud = longitud
        self.municipio = municipio
        self.telefono = telefono
        self.horario_apertura = horario_apertura
        self.horario_cierra = horario_cierre
        self.web = web
        self.nombre_archivo = nombre_archivo
        self.nombre_archivo_hasheado = nombre_archivo_hasheado
        self.estado = estado
        self.email = email
        self.enabled = 1
        self.disponible = disponible

    def save(self):
        db.session.add(self)
        db.session.commit()
        return True

    def actualizar(self):
        db.session.commit()
        return True

    @staticmethod
    def all():
        return Centro.query.all()

    def searchCenterByName(name):
        center = Centro.query.filter_by(nombre=name).first()
        if(center.count() == 1):
            return center
        else:
            return None

    def buscarPorId(unId):
        return Centro.query.filter_by(id=unId).first()

    def buscarHabilitados():
        consulta = db.session.query(Centro).filter_by(enabled=True)
        return consulta

    def buscarPendientes():
        consulta = db.session.query(Centro).filter_by(
            enabled=True, disponible=0)
        return consulta

    def obtenerTurnosPorIdCentroConMail(idCentro, email):
        return Centro.query.filter_by(idCentro)

    def obtenerTurnosPorIdCentro(idCentro):
        return Centro.obtenerTurnosPorIdCentro(idCentro)
        
    def buscarCriterio(busqueda,estado):
        if busqueda is not None and estado is not None:
            busqueda = busqueda +"%"
            consulta= db.session.query(Centro).filter(Centro.nombre.like(busqueda)).group_by(Centro.nombre,Centro.id).filter_by(enabled=True)
            consulta= consulta. filter_by(disponible=estado)
            return consulta 
        elif busqueda is not None:
            busqueda = busqueda +"%"
            consulta= db.session.query(Centro).filter(Centro.nombre.like(busqueda)).group_by(Centro.nombre,Centro.id).filter_by(enabled=True)
            return consulta 
        elif estado is not None:
            consulta= db.session.query(Centro).filter_by(enabled=True, disponible=estado)
            return consulta
        else:
            return db.session.query(Centro).filter_by(enabled=True)
    def disponibles():
        return Centro.query.filter_by(enabled=True,disponible=1,estado=1).all()