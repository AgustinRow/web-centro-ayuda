from app.db_sqlalchemy import db_sqlalchemy
from datetime import datetime
from app.models.rol import Rol
from werkzeug.security import check_password_hash
db = db_sqlalchemy
metadata = db.MetaData()


class Usuario(db.Model):
    __tablename__ = 'centros_usuarios'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    activo = db.Column(db.Integer)  # averiguar si es Integer o Boolean
    created_at = db.Column(db.DateTime(), nullable=True)
    updated_at = db.Column(db.DateTime(), nullable=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    enabled = db.Column(db.Integer)

    association_table = db.Table('centros_usuario_tiene_rol', metadata,
                                 db.Column('usuario_id', db.Integer,
                                           db.ForeignKey(id)),
                                 db.Column('rol_id', db.Integer, db.ForeignKey(Rol.id)))

    roles = db.relationship("Rol",
                            secondary=association_table,
                            )

    def __init__(self, nombre, apellido, email, password, username, rol):
        self.first_name = nombre
        self.last_name = apellido
        self.email = email
        self.password = password
        self.username = username
        self.enabled = 1
        self.activo = 1
        today = datetime.now()
        self.created_at = today.strftime("%Y-%m/%d, %H:%M:%S")
        self.updated_at = today.strftime("%Y-%m/%d, %H:%M:%S")
        roleInit = db.session.query(Rol).filter_by(nombre=rol).first()
        self.roles.append(roleInit)

    @staticmethod
    def all():
        return Usuario.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()
        return True

    def idUsuario(self):
        user = self.query.filter_by(email=self.email)
        iduser = user.first().id
        return iduser

    def imprimirRoles(self):
        roles = ""
        for each in self.roles:
            roles = roles+each.nombre+"\n"
        return roles

    def __repr__(self):
        return '<Usuario {0} {1} {2} {3} {4} {5} {6}>'.format(self.first_name,
                                                              self.last_name,
                                                              self.email,
                                                              self.password,
                                                              self.activo,
                                                              self.username,
                                                              imprimirRoles())

    # --- Desarrollo de Activar/Desactivar Usuario ---

    def buscarUsuarioPorID(id):
        user = Usuario.query.filter_by(id=id).first()
        return user

    def buscarEmailPassword(anEmail, aPassword):
        user = Usuario.query.filter_by(email=anEmail, activo=1, enabled=1)
        if user.count() == 1 and check_password_hash(user.first().password, aPassword):
            return user.first().idUsuario()
        else:
            return None

    def actualizar(self):
        db.session.commit()
        return True

    def buscarUsuarioPorEmail(email):
        user = Usuario.query.filter_by(email=email).first()
        return user

    def buscarUsuarioPorUsername(username):
        user = Usuario.query.filter_by(username=username).first()
        return user

    # --- busqueda de usuarios---
    def buscarHabilitados():
        consulta = db.session.query(Usuario).filter_by(enabled=True)
        return consulta

    def buscarXcriterio(busqueda):
        consulta = db.session.query(Usuario).filter(Usuario.username.like(
            busqueda)).group_by(Usuario.username).filter_by(enabled=True)
        return consulta

    def buscarActivosBloqueado(consulta, tipo):
        if tipo is 1:
            consulta = consulta.filter_by(activo=True)
        elif tipo is 0:
            consulta = consulta.filter_by(activo=False)
        return consulta
