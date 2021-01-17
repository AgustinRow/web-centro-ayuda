import os
from flask import request, render_template, url_for, redirect, flash, session, abort, send_file, send_from_directory, jsonify
from app.models.centro import Centro
from sqlalchemy import or_
from app.db_sqlalchemy import db_sqlalchemy
from app.helpers.auth import authenticated
from app.helpers.autsitio import sitioHabilitado, esOperador
from app.models.centro import Centro
from app.models.usuario import Usuario
from app.resources import tipoCentro, rol, sitio
from datetime import datetime, time
from flask import current_app
from werkzeug.utils import secure_filename
from datetime import time
import uuid
from app.resources.error_handling import InternalServer, BadRequest
from app.view.centroView import CentroView
from werkzeug.datastructures import ImmutableMultiDict


def verificarSesion():
    if not authenticated(session):
        abort(401)


def verificarPermisoPara(unPermiso):
    result = False
    usuarioEnSesion = Usuario.buscarUsuarioPorID(session["id"])
    for miRol in usuarioEnSesion.roles:
        if(rol.tienePermiso(unPermiso, miRol.id)):
            result = True
    return result


def busqueda():
    if sitioHabilitado(session):
        verificarSesion()
        form = request.form
        busqueda = form["buscar"]
        return redirect(url_for("listado_centros", busqueda=busqueda, page=1))
    else:
        if 'id' in session:
            del session['id']
        flash("Sitio temporalmente deshabilitado al publico", "error")
        abort(401)


def listado():
    if sitioHabilitado(session):
        verificarSesion()
        # centros = Centro.all()
        if (verificarPermisoPara("centro_index")):
            page = int(request.args.get('page', '1'))
            busqueda = request.args.get('busqueda', None)
            filtro = request.args.get('filtro', None)
            rtabusqueda = Centro.buscarCriterio(busqueda, filtro)
            cant_elem = sitio.obtenerElementosPorPagina()
            rtabusqueda = rtabusqueda.paginate(page, cant_elem, False)
            return render_template("listado_centros.html", centros=rtabusqueda, busqueda=busqueda, filtro=filtro)
    else:
        if 'id' in session:
            del session['id']
        flash("Sitio temporalmente deshabilitado al publico", "error")
        return redirect(url_for("usuario_login"))


def all():
    return Centro.all()


def nuevo_centro():
    if(sitioHabilitado(session)):
        verificarSesion()
        if(verificarPermisoPara("centro_new")):
            tipo = tipoCentro.all()
            return render_template("nuevo_centro.html", tipos=tipo)
        flash("Sin Permiso para realizar accion")
        centros = Centro.all()
        return render_template("listado_centros.html", centros=centros)
    else:
        if 'id' in session:
            del session['id']
        flash("Sitio temporalmente deshabilitado al publico", "error")
        return redirect(url_for("usuario_login"))


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['pdf'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def buscarCentroPorNombre(nombre):
    return Centro.searchCenterByName(nombre)

# Sube el archivo a la carperta destino y retorna el nombre del mismo


def uploadFile(file):
    if file.filename == '':
        file_name = ''
    else:
        if file and allowed_file(file.filename):
            file_name = uuid.uuid4().hex
            file_name = file_name + ".pdf"
            file_path = os.path.join(
                "app/", current_app.config['UPLOAD_FOLDER'], file_name)
            file.save(file_path)
            print(file_path)
    return file_name


def toogleState(id):
    if(sitioHabilitado(session)):
        if(verificarPermisoPara("centro_update")):
            centro = Centro.buscarPorId(id)
            centro.estado = 1 - centro.estado
            Centro.save(centro)
            if(centro.estado == 1):
                flash("Centro publicado exitosamente", "success")
            else:
                flash("Centro despublicado ", "error")
        return redirect(url_for("listado_centros", page=1))
    else:
        if 'id' in session:
            del session['id']
        flash("Sitio temporalmente deshabilitado al publico", "error")
        abort(401)


def create():
    if sitioHabilitado(session):
        if(verificarPermisoPara("centro_new")):
            centerDetails = request.form
            nombre = centerDetails['nombreCentro']
            direccion = centerDetails['direccionCentro']
            telefono = centerDetails['telefonoCentro']
            categoria = centerDetails.get('tipoCentro')
            municipio = centerDetails.get('municipioCentro')
            web = centerDetails['webCentro']
            email = centerDetails['emailCentro']
            horaApertura = centerDetails['horaApertura']
            horaCierre = centerDetails['horaCierre']
            if(esOperador(session)):
                disponible = 1  # aceptad
                estado = 1  # publicado
            else:
                disponible = 0  # pendiente
                estado = 0  # despublicado
            latitud = centerDetails['latitudCentro']
            longitud = centerDetails['longitudCentro']
            file = request.files['inputFile']
            file_name_hashed = uploadFile(file)
            nombre_archivo = secure_filename(file.filename)
            new_center = Centro(nombre, direccion, categoria, telefono,
                                municipio, web, file_name_hashed, estado, latitud, longitud, horaApertura, horaCierre, email, disponible, nombre_archivo)
            new_center.save()
            return redirect(url_for("listado_centros", page=1))
        else:
            flash("Sin permisos para creacion de un centro", "error")
    else:
        if 'id' in session:
            del session['id']
        flash("Sitio temporalmente deshabilitado al publico", "error")
        abort(401)


def downloadFile(filename):
    directory = os.path.join(
        current_app.config['UPLOAD_FOLDER'])
    print(str(directory))
    return send_from_directory(directory, filename)


def buscarPorId(id):
    return Centro.buscarPorId(id)


def delete(id):
    if(sitioHabilitado(session)):
        if(verificarPermisoPara("centro_destroy")):
            centro = Centro.buscarPorId(id)
            centro.enabled = 0
            Centro.save(centro)
            flash("Centro " + centro.nombre +
                  " eliminado exitosamente", 'success')
        else:
            flash(
                "No se puede eliminar usuario porque no se tienen permisos necesarios", 'error')
        centros = Centro.all()
        return redirect(url_for("listado_centros", page=1))
    else:
        if 'id' in session:
            del session['id']
        flash("Sitio temporalmente deshabilitado al publico", "error")
        abort(401)


def edit(id):
    if(sitioHabilitado(session)):
        if(verificarPermisoPara("centro_update")):
            tipo = tipoCentro.all()
            centro = Centro.buscarPorId(id)
            return render_template("editar_centro.html", centro=centro, tipos=tipo)
    else:
        if 'id' in session:
            del session['id']
        flash("Sitio temporalmente deshabilitado al publico", "error")
        abort(401)


def manageState():
    if sitioHabilitado(session):
        page = int(request.args.get('page', '1'))
        rtabusqueda = Centro.buscarPendientes()
        cant_elem = sitio.obtenerElementosPorPagina()
        rtabusqueda = rtabusqueda.paginate(page, cant_elem, False)
        return render_template("centros_administracion.html", centros=rtabusqueda)
    else:
        if 'id' in session:
            del session['id']
        flash("Sitio temporalmente deshabilitado al publico", "error")
        abort(401)


def guardarEdicion(id):
    if sitioHabilitado(session):
        if(verificarPermisoPara("centro_update")):
            centro = Centro.buscarPorId(id)
            centerDetails = request.form
            centro.nombre = centerDetails['nombreCentro']
            centro.direccion = centerDetails['direccionCentro']
            centro.telefono = centerDetails['telefonoCentro']
            centro.categoria = centerDetails.get('tipoCentro')
            centro.municipio = centerDetails.get('municipioCentro')
            centro.web = centerDetails['webCentro']
            centro.email = centerDetails['emailCentro']
            centro.horaApertura = centerDetails['horaApertura']
            centro.horaCierra = centerDetails['horaCierre']
            if(esOperador(session)):
                centro.disponible = 1
                centro.estado = True
            else:
                centro.disponible = 0
                centro.estado = False
            centro.latitud = centerDetails['latitudCentro']
            centro.longitud = centerDetails['longitudCentro']
            if(request.files['inputFile'].filename):
                file = request.files['inputFile']
                centro.nombre_archivo_hasheado = uploadFile(file)
                centro.nombre_archivo = file.filename
            Centro.save(centro)
            flash("Los cambios se realizaron con exito!", 'success')
            return redirect(url_for("listado_centros", page=1))
        else:
            flash("Sin permisos para la edicion de centro", "error")
    else:
        if 'id' in session:
            del session['id']
        flash("Sitio temporalmente deshabilitado al publico", "error")
        abort(401)


def aceptarCargaCentro(id):
    if sitioHabilitado(session):
        if(verificarPermisoPara("centro_update")):
            centro = Centro.buscarPorId(id)
            centro.disponible = 1
            Centro.save(centro)
            return redirect(url_for("listado_centros",  page=1))
    else:
        if 'id' in session:
            del session['id']
        flash("Sitio temporalmente deshabilitado al publico", "error")
        abort(401)


def rechazarCargaCentro(id):
    if sitioHabilitado(session):
        if(verificarPermisoPara("centro_update")):
            centro = Centro.buscarPorId(id)
            centro.disponible = 2
            Centro.save(centro)
            return redirect(url_for("listado_centros", page=1))
    else:
        if 'id' in session:
            del session['id']
        flash("Sitio temporalmente deshabilitado al publico", "error")
        abort(401)


def obtenerTurnosPorIdCentroConMail(idCentro, email):
    return Centro.obtenerTurnosPorIdCentroConMail(idCentro, email)


def obtenerTurnosPorIdCentro(idCentro):
    return Centro.obtenerTurnosPorIdCentro(idCentro)


def centrosDisponibles():
    return Centro.disponibles()


def getCentrosApi():
    try:
        centros_schema = CentroView(many=True)
        centros = centrosDisponibles()
        resultado = centros_schema.dump(centros, many=True)
        total = len(centros)
        cant_elem = sitio.obtenerElementosPorPagina()
        return jsonify(centros=resultado, total=total, per_page=cant_elem)
    except Exception:
        raise InternalServer('Internal server error')


def getCentrosIdApi(centro_id):
    try:
        centro = Centro.buscarPorId(centro_id)
        if centro is None:
            return jsonify({"message": "No se pudo encontrar el centro con id " + str(centro_id)}), 404
        centro_schema = CentroView()
        resultado = centro_schema.dump(centro)
        return jsonify(atributos=resultado), 200
    except:
        raise InternalServer('Internal server error')

def postCentrosApi():
    try:
        nombre = request.json['nombre']
        direccion = request.json['direccion']
        telefono = request.json['telefono']
        hora_apertura = request.json['hora_apertura']
        hora_cierre = request.json['hora_cierre']
        tipo = request.json['tipo']
        web = request.json['web']
        email = request.json['email']
        latitud=request.json['latitud']
        longitud=request.json['longitud']
        municipio=request.json['municipio']

        new_center = Centro(nombre, direccion, tipo, telefono,
                            municipio, web, 'file_name', False, latitud, longitud, hora_apertura, hora_cierre, email, 0,'file_name')
        new_center.save()
        centro_schema = CentroView()
        resultado = centro_schema.dump(new_center)
        return jsonify(atributos=resultado), 201
    except KeyError:
        raise BadRequest('BadRequest')
    except Exception:
        raise InternalServer('Internal server error')