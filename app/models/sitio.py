from app.db_sqlalchemy import db_sqlalchemy
db = db_sqlalchemy
metadata = db.MetaData()


class Sitio(db.Model):
    __tablename__ = 'centros_site_configuration'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255))
    elementos_por_pagina = db.Column(db.Integer)
    introduccion = db.Column(db.Text)
    contacto_telefono = db.Column(db.String(255))
    contacto_email = db.Column(db.String(255))
    habilitado_al_publico = db.Column(db.Boolean)


    def __repr__(self):
        return '<Config {0} {1} {2} {3} {4} {5}>'.format(self.titulo,
                                                              self.elementos_por_pagina,
                                                              self.introduccion,
                                                              self.contacto_telefono,
                                                              self.contacto_email,
                                                              self.habilitado_al_publico)
    
    def obtenerConfiguracion():
        config = Sitio.query.get(1)
        return config

    def obtenerTitulo():
        titulo = Sitio.query.get(1).titulo
        return titulo
    
    def obtenerElementosPorPagina():
        cant = Sitio.query.get(1).elementos_por_pagina
        return cant
    
    def obtenerIntroduccion():
        intro = Sitio.query.get(1).introduccion
        return intro
    
    def obtenerTelefono():
        tel = Sitio.query.get(1).contacto_telefono
        return tel
    
    def obtenerMail():
        mail = Sitio.query.get(1).contacto_email
        return mail
    
    def obtenerHabilitadoAlPublico():
        hab = Sitio.query.get(1).habilitado_al_publico
        return hab

    def save(self):
        db.session.commit()
        return True
    