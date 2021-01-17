from flask import request, render_template, redirect, url_for, flash, abort, session
from app.models.sitio import Sitio
from app.helpers.auth import authenticated
from app.helpers.autsitio import sitioHabilitado
from app.resources import usuario, rol
from app.models.usuario import Usuario


def verificarSesion():
    if not authenticated(session):
        abort(401)


def obtenerTitulo():
    return Sitio.obtenerTitulo()


def obtenerElementosPorPagina():
    return Sitio.obtenerElementosPorPagina()


def obtenerIntroduccion():
    return Sitio.obtenerIntroduccion()


def obtenerTelefono():
    return Sitio.obtenerTelefono()


def obtenerMail():
    return Sitio.obtenerMail()


def obtenerHabilitadoAlPublico():
    return Sitio.obtenerHabilitadoAlPublico()


def configSitio():
    if sitioHabilitado(session):
        verificarSesion()
        usuarioEnSesion = Usuario.buscarUsuarioPorID(session["id"])
        for miRol in usuarioEnSesion.roles:
            if (rol.permisoModificarConfiguracion(miRol.id)):
                sitio = Sitio.obtenerConfiguracion()
                return render_template("configuracion_sitio.html", sitio=sitio)
        flash("No tiene permisos para ingresar al area de configuracion.", "error")
        return redirect(url_for("usuario_listado"))
    else:
        if 'id' in session:
            del session['id']
        abort(401)


def actualizarInfo():
    if sitioHabilitado(session):
        verificarSesion()

        if not usuario.soyAdministrador(session.get("id")):
            flash("No tiene permisos para ingresar al area de configuracion.", "error")
            return redirect(url_for("usuario_listado"))

        sitio = Sitio.obtenerConfiguracion()
        data = request.form
        check = validarInfo(data)
        if check:
            sitio.titulo = data['titulo']
            sitio.elementos_por_pagina = data['elementos_por_pagina']
            sitio.introduccion = data['introduccion']
            sitio.contacto_telefono = data['telefono']
            sitio.contacto_email = data['email']
            sitio.save()
            flash("¡Configuracion actualizada con exito!", "success")
        else:
            flash("Error, no puede dejar datos sin completar", "error")
        return redirect(url_for("configuracion_sitio"))
    else:
        if 'id' in session:
            del session['id']
        abort(401)


def validarInfo(data):
    titulo = data['titulo']
    introduccion = data['introduccion']
    contacto_telefono = data['telefono']
    contacto_email = data['email']

    if titulo.strip() == "" or introduccion.strip() == "" or contacto_telefono.strip() == "" or contacto_email.strip() == "":
        return False
    else:
        return True


def modificarHabilitacion():
    if sitioHabilitado(session):
        verificarSesion()
        if usuario.soyAdministrador(session.get("id")):
            sitio = Sitio.obtenerConfiguracion()
            sitio.habilitado_al_publico = not(sitio.habilitado_al_publico)
            sitio.save()
            flash("¡Habilitacion del sitio modificada con exito!", "success")
    return redirect(url_for("configuracion_sitio"))
