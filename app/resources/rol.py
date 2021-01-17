from flask import request, render_template, redirect, url_for, session, jsonify
from app.models.rol import Rol
from app.models.usuario import Usuario
from app.resources import permiso
from sqlalchemy import or_
from app.db_sqlalchemy import db_sqlalchemy


def verificarPermisoPara(unPermiso):
    result = False
    usuarioEnSesion = Usuario.buscarUsuarioPorID(session["id"])
    for miRol in usuarioEnSesion.roles:
        if(tienePermiso(unPermiso, miRol.id)):
            result = True
    return result


def tienePermiso(permiso, id):
    rol = Rol.buscarRolPorId(id)
    for miPermiso in rol.permisos:
        if(miPermiso.nombre == permiso):
            return True
    return False


def buscarRolPorId(id):
    return Rol.buscarRolPorId(id)


def index():
    listaRoles = all()
    return render_template("roles.html", roles=listaRoles)


def all():
    return Rol.all()


def create():
    if request.method == 'POST':
        rolDetails = request.form
        nombre = rolDetails["nombreRol"]
        new_rol = Rol(nombre)
        new_rol.save()
    return redirect(url_for("rol_index"))


def permisoEliminar(id):
    rol = Rol.buscarRolPorId(id)
    for miPermiso in rol.permisos:
        if(permiso.destroy(miPermiso.id)):
            return True
    return False


def permisoModificar(id):
    rol = Rol.buscarRolPorId(id)
    for miPermiso in rol.permisos:
        if(permiso.update(miPermiso.id)):
            return True
    return False


def permisoCreacion(id):
    rol = Rol.buscarRolPorId(id)
    for miPermiso in rol.permisos:
        if(permiso.new(miPermiso.id)):
            return True
    return False


def permisoEditar(id):
    rol = Rol.buscarRolPorId(id)
    for miPermiso in rol.permisos:
        if(permiso.update(miPermiso.id)):
            return True
    return False


def permisoAccesoConfiguracion(id):
    rol = Rol.buscarRolPorId(id)
    for miPermiso in rol.permisos:
        if(permiso.indexConfig(miPermiso.id)):
            return True
    return False


def permisoModificarConfiguracion(id):
    rol = Rol.buscarRolPorId(id)
    for miPermiso in rol.permisos:
        if(permiso.updateConfig(miPermiso.id)):
            return True
    return False
