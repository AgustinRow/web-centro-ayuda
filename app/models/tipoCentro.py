from app.db_sqlalchemy import db_sqlalchemy

db = db_sqlalchemy


class TipoCentro (db.Model):
    __tablename__ = 'centros_tipo'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))

    def __inti__(self, nombre):
        self.nombre = nombre

    def all():
        return db.session.query(TipoCentro).all()

    def __repr__(self):
        return '<TipoCentro {0}>'.format(self.nombre)

    def buscarTipoCentroPorId(id):
        return db.session.query(TipoCentro).filter_by(id=id).first()

    def getNombre(id):
        return TipoCentro.buscarPermisoPorId(id).nombre
