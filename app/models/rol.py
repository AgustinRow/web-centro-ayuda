from app.db_sqlalchemy import db_sqlalchemy
from app.models.permiso import Permiso

db = db_sqlalchemy
metadata = db.MetaData()


class Rol (db.Model):
    __tablename__ = 'centros_rol'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))

    association_table = db.Table('centros_rol_tiene_permiso', metadata,
                                 db.Column('rol_id', db.Integer,
                                           db.ForeignKey(id)),
                                 db.Column('permiso_id', db.Integer, db.ForeignKey(Permiso.id)))

    permisos = db.relationship("Permiso",
                               secondary=association_table,
                               )

    ########################
    # Rol.asignarPermisos() no hace nada???
    def __init__(self, valor_nombre):
        self.nombre = valor_nombre
        if(valor_nombre == "Administrador"):
            Rol.asignarPermisosAdmin()
        else:
            Rol.asignarPermisosOperador()
        db.session.commit()

    def __repr__(self):
        return '<Rol {0}>'.format(self.nombre)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return True

    def all():
        return db.session.query(Rol).all()

    def buscarRolPorId(id):
        return db.session.query(Rol).filter_by(id=id).first()
