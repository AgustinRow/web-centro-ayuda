from app.helpers.auth import authenticated
from app.models.sitio import Sitio
from app.models.usuario import Usuario
from app.resources import rol
from flask import session


def sitioHabilitado(session):
    return Sitio.obtenerHabilitadoAlPublico() or esAdministrador(session)


def esAdministrador(session):
    if authenticated(session):
        user = Usuario.buscarUsuarioPorID(session.get("id"))
        admin = False
        for each in user.roles:
            if each.nombre == "Administrador":
                admin = True
                break
        return admin
    else:
        return False


def esOperador(session):
    if authenticated(session):
        user = Usuario.buscarUsuarioPorID(session.get("id"))
        admin = False
        for each in user.roles:
            if each.nombre == "Operador":
                admin = True
                break
        return admin
    else:
        return False
