from flask import request, render_template, redirect, url_for, session
from app.models.permiso import Permiso
#from sqlalchemy import or_
#from app.db_sqlalchemy import db_sqlalchem


def buscarPermisoPorId(id):
    return Permiso.buscarPermisoPorId(id)


def getNombre(id):
    return Permiso.getNombre(id)


def destroy(id):
    permiso = buscarPermisoPorId(id)
    if(permiso.nombre == "usuario_destroy"):
        return True
    else:
        return False


def index(id):
    permiso = buscarPermisoPorId(id)
    if(permiso.nombre == "usuario_index"):
        return True
    else:
        return False


def show(id):
    permiso = buscarPermisoPorId(id)
    if(permiso.nombre == "usuario_show"):
        return True
    else:
        return False


def update(id):
    permiso = buscarPermisoPorId(id)
    if(permiso.nombre == "usuario_update"):
        return True
    else:
        return False


def new(id):
    permiso = buscarPermisoPorId(id)
    if(permiso.nombre == "usuario_new"):
        return True
    else:
        return False


def indexConfig(id):
    permiso = buscarPermisoPorId(id)
    if(permiso.nombre == "config_index"):
        return True
    else:
        return False


def showConfig(id):
    permiso = buscarPermisoPorId(id)
    if(permiso.nombre == "config_show"):
        return True
    else:
        return False


def updateConfig(id):
    permiso = buscarPermisoPorId(id)
    if(permiso.nombre == "config_update"):
        return True
    else:
        return False
