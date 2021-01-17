from flask import request, render_template, url_for, redirect, flash, session, abort
from app.models.usuario import Usuario
from app.resources import rol, sitio, turno
from sqlalchemy import or_
from app.db_sqlalchemy import db_sqlalchemy
from datetime import datetime, timedelta
from app.helpers.auth import authenticated
from app.helpers.autsitio import sitioHabilitado
from werkzeug.security import generate_password_hash


def verificarSesion():
    if not authenticated(session):
        abort(401)


def all():
    return Usuario.all()


def buscarPorId(unId):
    return Usuario.buscarUsuarioPorID(unId)


def autenticarlogin():
    datosUsuario = request.form
    email = datosUsuario["email"]
    password = datosUsuario["password"]
    idUser = Usuario.buscarEmailPassword(email, password)
    if idUser is not None:
        session["id"] = idUser
        session["username"] = Usuario.buscarUsuarioPorID(idUser).username
        if soyAdministrador(idUser):
            session["configPermitido"] = 1
        else:
            session["configPermitido"] = 0  
            
        if soyOperador(idUser):
            session["operador"] = True
            session["turnos"] = 1
        else:
            session["operador"] = False
            session["turnos"] = 0
    else:
        flash("Correo o Contraseña Incorrectos", "error")
        return redirect(url_for("usuario_login"))
    if sitioHabilitado(session):
        return redirect(url_for("home"))
    else:
        if 'id' in session:
            del session['id']
        flash("Sitio temporalmente deshabilitado al publico", "error")
        return redirect(url_for("usuario_login"))


def login():
    if authenticated(session):
        return redirect(url_for("home"))
    return render_template("loginUser.html")


def logout():
    if sitioHabilitado(session):
        if authenticated(session):
            del session['id']
        return redirect(url_for("usuario_login"))
    else:
        if 'id' in session:
            del session['id']
        flash("Sitio temporalmente deshabilitado al publico", "error")
        abort(401)


def comprobarDatos(data):
    resultado = [True, ""]
    email = data['emailUsuario']
    username = data['usernameUsuario']
    emailExiste = Usuario.buscarUsuarioPorEmail(email=email)
    usernameExiste = Usuario.buscarUsuarioPorUsername(username=username)

    if(emailExiste is not None):
        resultado[0] = False
        resultado[1] = "Email ya registrado en la Base de Datos"

    if(usernameExiste is not None):
        if(resultado[0]):
            resultado[0] = False
            resultado[1] = "Username ya registrado en la Base de Datos"
        else:
            resultado[1] = resultado[1] + \
                "\nUsername ya registrado en la Base de Datos"
    return resultado


def perfil():
    if sitioHabilitado(session):
        verificarSesion()
        return render_template("miperfil.html", id=session["id"])
    else:
        if 'id' in session:
            del session['id']
        flash("Sitio temporalmente deshabilitado al publico", "error")
        abort(401)


def create():
    if sitioHabilitado(session):
        verificarSesion()
        usuarioEnSesion = Usuario.buscarUsuarioPorID(session["id"])
        for miRol in usuarioEnSesion.roles:
            if(rol.permisoCreacion(miRol.id)):
                userDetails = request.form
                check = comprobarDatos(userDetails)
                if check[0]:
                    nombre = userDetails['nombreUsuario']
                    apellido = userDetails['apellidoUsuario']
                    email = userDetails['emailUsuario']
                    username = userDetails['usernameUsuario']
                    password = generate_password_hash(
                        userDetails['passwordUsuario'], "sha256", 25)
                    rolUsuario = userDetails['rolUsuario']
                    new_user = Usuario(nombre, apellido, email,
                                       password, username, rolUsuario)
                    new_user.save()
                    flash("¡Usuario generado con exito!", "success")
                else:
                    flash(check[1], "error")
                return redirect(url_for("usuario_listado", page=1))
        flash("No tienes permisos para crear un nuevo usuario", "error")
        return redirect(url_for("usuario_listado", page=1))

    else:
        if 'id' in session:
            del session['id']
        flash("Sitio temporalmente deshabilitado al publico", "error")
        abort(401)


def modificarEstado(id):
    if sitioHabilitado(session):
        verificarSesion()
        if(id != session["id"]):
            user = Usuario.buscarUsuarioPorID(id)
            usuarioEnSesion = Usuario.buscarUsuarioPorID(session["id"])
            for miRol in usuarioEnSesion.roles:
                if(rol.tienePermiso("usuario_update", miRol.id)):
                    for each in user.roles:
                        if each.nombre == "Administrador":
                            flash(
                                "No se puede bloquear un usuario con rol Administrador", "error")
                            return redirect(url_for("usuario_listado", page=1))
                    user.activo = 1 - user.activo
                    Usuario.actualizar(user)
                    if(user.activo):
                        flash("Usuario " + user.username +
                              " activado", 'success')
                    else:
                        flash("Usuario " + user.username +
                              " desactivado", 'success')
                    return redirect(url_for("usuario_listado", page=1))
            flash("Sin permisos para bloquear usuario", 'error')
        else:
            flash("No podes bloquearte a vos mismo", 'error')
        return redirect(url_for("usuario_listado", page=1))
    else:
        if 'id' in session:
            del session['id']
        flash("Sitio temporalmente deshabilitado al publico", "error")
        abort(401)


def delete(id):
    if sitioHabilitado(session):
        verificarSesion()
        user = Usuario.buscarUsuarioPorID(id)
        if(id != session["id"]):
            user = Usuario.buscarUsuarioPorID(id)
            usuarioEnSesion = Usuario.buscarUsuarioPorID(session["id"])
            for miRol in usuarioEnSesion.roles:
                if(rol.permisoEliminar(miRol.id)):
                    user.enabled = 0
                    Usuario.actualizar(user)
                    flash("Usuario " + user.username + " eliminado", 'success')
                    return redirect(url_for("usuario_listado", page=1))
            flash(
                "No se puede eliminar usuario porque no se tienen permisos necesarios", 'error')
        else:
            flash("El usuario intento eliminarse a si mismo", 'error')
        return redirect(url_for("usuario_listado", page=1))
    else:
        if 'id' in session:
            del session['id']
        flash("Sitio temporalmente deshabilitado al publico", "error")
        abort(401)


def editar(id):
    if sitioHabilitado(session):
        verificarSesion()
        usuarioEnSesion = Usuario.buscarUsuarioPorID(session["id"])
        user = Usuario.buscarUsuarioPorID(id)
        for miRol in usuarioEnSesion.roles:
            if(rol.permisoEditar(miRol.id)):
                return render_template("editarUsuario.html", user=user)
        flash("No tiene permisos para editar", "error")
        return redirect(url_for("usuario_listado"))
    else:
        if 'id' in session:
            del session['id']
        flash("Sitio temporalmente deshabilitado al publico", "error")
        abort(401)


def guardarEdicion(id):
    if sitioHabilitado(session):
        verificarSesion()

        usuarioEnSesion = Usuario.buscarUsuarioPorID(session["id"])
        permiso = False
        for miRol in usuarioEnSesion.roles:
            if(rol.permisoEditar(miRol.id)):
                permiso = True
                break
        if not permiso:
            flash("No tiene permisos para editar", "error")
            return redirect(url_for("usuario_listado"))

        userDetails = request.form
        user = Usuario.buscarUsuarioPorID(id)
        cambio = verificarCambios(user, userDetails)
        if cambio[0]:
            if cambio[1] == 0:
                user.first_name = userDetails['nombreUsuario']
                user.last_name = userDetails['apellidoUsuario']
                user.email = userDetails['emailUsuario']
                user.username = userDetails['usernameUsuario']
                today = datetime.now()
                user.updated_at = today.strftime("%Y-%m/%d, %H:%M:%S")
                Usuario.actualizar(user)
                flash("Los cambios se realizaron con exito!", 'success')
            else:
                flash(cambio[2], 'error')
        else:
            flash("No se realizo ningun cambio en la informacion del usuario", 'warning')

        return redirect(url_for("usuario_listado", page=1))
    else:
        if 'id' in session:
            del session['id']
        flash("Sitio temporalmente deshabilitado al publico", "error")
        abort(401)


def verificarCambios(user, userData):
    nombre = user.first_name != userData["nombreUsuario"].strip()
    apellido = user.last_name != userData["apellidoUsuario"].strip()
    email = user.email != userData["emailUsuario"].strip()
    username = user.username != userData["usernameUsuario"].strip()
    resultado = [False, -1, ""]

    if (nombre or apellido) and (userData["nombreUsuario"].strip() != "") and (userData["apellidoUsuario"].strip() != ""):
        resultado = [True, 0, ""]

    if email and (userData["emailUsuario"].strip() != ""):
        usu = Usuario.buscarUsuarioPorEmail(userData["emailUsuario"])
        if usu is not None:
            resultado = [True, 1, "Email ingresado ya existe en el sistema"]
        else:
            resultado = [True, 0, ""]
    if username and (userData["usernameUsuario"].strip() != ""):
        usu = Usuario.buscarUsuarioPorUsername(userData["usernameUsuario"])
        if usu is not None:
            resultado = [True, 1, "Username ingresado ya existe en el sistema"]
        else:
            resultado = [True, 0, ""]
    return resultado


def busqueda():
    if sitioHabilitado(session):
        verificarSesion()
        form = request.form
        busqueda = form["buscar"]
        return redirect(url_for("usuario_listado", valor=busqueda, page=1))
    else:
        if 'id' in session:
            del session['id']
        flash("Sitio temporalmente deshabilitado al publico", "error")
        abort(401)


def listado():
    if sitioHabilitado(session):
        verificarSesion()
        page = int(request.args.get('page', '1'))
        valor = request.args.get('valor', None)
        tipo = request.args.get('tipo', None)
        if tipo is not None:
            tipo = int(tipo)
        if valor is None and tipo is None:
            rtabusqueda = Usuario.buscarHabilitados()
        elif valor is not None:
            valor = valor+"%"
            rtabusqueda = Usuario.buscarXcriterio(valor)
            if tipo is not None:
                rtabusqueda = Usuario.buscarActivosBloqueado(rtabusqueda, tipo)
        elif tipo is not None and valor is None:
            rtabusqueda = Usuario.buscarHabilitados()
            rtabusqueda = Usuario.buscarActivosBloqueado(rtabusqueda, tipo)
        cant_elem = sitio.obtenerElementosPorPagina()
        rtabusqueda = rtabusqueda.paginate(page, cant_elem, False)
        roles = rol.all()
        return render_template("listado_usuarios.html", users=rtabusqueda, busqueda=valor, tipo=tipo, roles=roles)
    else:
        if 'id' in session:
            del session['id']
        abort(401)


def asignarRoles(id):
    if sitioHabilitado(session):
        verificarSesion()

        usuarioEnSesion = Usuario.buscarUsuarioPorID(session["id"])
        permiso = False
        for miRol in usuarioEnSesion.roles:
            if(rol.permisoEditar(miRol.id)):
                permiso = True
                break
        if not permiso:
            flash("No tiene permisos para asignar roles", "error")
            return redirect(url_for("usuario_listado"))

        usu = Usuario.buscarUsuarioPorID(id)
        roles_usuario = usu.roles
        roles = rol.all()
        for each in roles_usuario:
            roles.remove(each)
        return render_template("asignarRolesUsuario.html", rolesU=roles_usuario, roles=roles, idUser=id, usernameUser=usu.username)
    else:
        if 'id' in session:
            del session['id']
        abort(401)


def actualizarRoles(id):
    if sitioHabilitado(session):
        verificarSesion()

        usuarioEnSesion = Usuario.buscarUsuarioPorID(session["id"])
        permiso = False
        for miRol in usuarioEnSesion.roles:
            if(rol.permisoEditar(miRol.id)):
                permiso = True
                break
        if not permiso:
            flash("No tiene permisos para asignar roles", "error")
            return redirect(url_for("usuario_listado"))

        roles = rol.all()
        data = request.form
        rolesUsuario = []

        session["configPermitido"] = 0
        session["operador"] = False
        session["turnos"] = 0

        for each in roles:
            if each.nombre in request.form:
                if data[each.nombre] == "on":
                    if each.nombre == "Administrador":
                        session["configPermitido"] = 1
                    if each.nombre == "Operador":
                        session["operador"] = True
                        session["turnos"] = 1

                    rolesUsuario.append(each)

        if len(rolesUsuario) == 0:
            flash("No se puede dejar un usuario sin roles asignados", "error")
            return redirect(url_for("usuario_roles", id=id))

        user = Usuario.buscarUsuarioPorID(id)
        user.roles = rolesUsuario
        user.save()

        flash("¡Los roles se asignaron con exito!", "success")
        return redirect(url_for("usuario_listado"))

    else:
        if 'id' in session:
            del session['id']
        abort(401)

def soyAdministrador(id):
    user = Usuario.buscarUsuarioPorID(id)
    for each in user.roles:
        if each.nombre == "Administrador":
            return True
    return False


def soyOperador(id):
    user = Usuario.buscarUsuarioPorID(id)
    for each in user.roles:
        if each.nombre == "Operador":
            return True
    return False
