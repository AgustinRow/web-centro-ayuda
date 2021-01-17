from app.db_sqlalchemy import db_sqlalchemy
from datetime import datetime
db = db_sqlalchemy


class Permiso(db.Model):
    __tablename__ = "centros_permisos"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))

    def __inti__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return '<Permisos {0}>'.format(self.nombre)

    # Repito codigo. Dont Repeat Yourself

    def buscarPermisoPorId(id):
        return db.session.query(Permiso).filter_by(id=id).first()

    def getNombre(id):
        return Permiso.buscarPermisoPorId(id).nombre
