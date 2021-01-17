from os import path, environ
from flask import Flask, render_template, g, session, redirect, url_for, jsonify
from flask_session import Session
from config import config
from app import db
from app.resources import issue
from app.resources import user
from app.resources import auth
from app.resources.api import issue as api_issue
from app.helpers import handler
from app.helpers import auth as helper_auth
from dotenv import load_dotenv
from app.db_sqlalchemy import db_sqlalchemy
from app.resources import usuario, rol, centro, sitio, turno
from flask import request
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from app.resources.error_handling import InternalServer, BadRequest
from flask_cors import CORS,cross_origin

def create_app(environment="development"):
    load_dotenv()

    # Configuración inicial de la app
    app = Flask(__name__)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    
    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    Bootstrap(app)

    # Configure db
    db.init_app(app)

    # Configure sqlAlchemy
    conf = app.config
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://" + \
        conf["DB_USER"]+":"+conf["DB_PASS"]+"@" + \
        conf["DB_HOST"]+"/"+conf["DB_NAME"]
    db_sqlalchemy.init_app(app)

    # Configure secure_filename
    UPLOAD_FOLDER = 'static/uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)

    # Autenticación
    app.add_url_rule("/iniciar_sesion", "auth_login", auth.login)
    app.add_url_rule("/cerrar_sesion", "auth_logout", auth.logout)
    app.add_url_rule("/autenticacion", "auth_authenticate",
                     auth.authenticate, methods=["POST"])

    # Rutas de Consultas
    app.add_url_rule("/consultas", "issue_index", issue.index)
    app.add_url_rule("/consultas", "issue_create",
                     issue.create, methods=["POST"])
    app.add_url_rule("/consultas/nueva", "issue_new", issue.new)

    # Rutas de UsuariosCatedra
    app.add_url_rule("/usuariosCatedra", "user_index", user.index)
    app.add_url_rule("/usuariosCatedra", "user_create",
                     user.create, methods=["POST"])
    app.add_url_rule("/usuariosCatedra/nuevo", "user_new", user.new)

    # Rutas para Usuarios
    app.add_url_rule("/usuarios/nuevo", "usuario_create",
                     usuario.create, methods=["POST"])
    app.add_url_rule("/login", "usuario_login", usuario.login)
    app.add_url_rule("/login", "usuario_autenticar",
                     usuario.autenticarlogin, methods=["POST"])
    app.add_url_rule("/logout", "usuario_logout", usuario.logout)
    app.add_url_rule("/Account", "usuario_perfil", usuario.perfil)

    # --- activar/desactivar usuarios ---
    app.add_url_rule("/usuarios/modificarEstadoUsuario/<int:id>",
                     "usuario_cambiar_estado", usuario.modificarEstado)

    # --- eliminar usuarios ---
    app.add_url_rule("/usuarios/eliminarUsuario/<int:id>",
                     "usuario_eliminar", usuario.delete)
    # ----editar usuarios
    app.add_url_rule("/usuarios/editar/<int:id>",
                     "usuario_editar", usuario.editar)
    app.add_url_rule("/usuarios/guardarCambios/<int:id>", "usuario_guardar_edicion",
                     usuario.guardarEdicion, methods=["POST"])

    app.add_url_rule("/usuarios/actualizar-roles/<int:id>",
                     "usuario_actualizar_roles", usuario.actualizarRoles, methods=["POST"])
    app.add_url_rule("/usuarios/asignarRoles/<int:id>",
                     "usuario_roles", usuario.asignarRoles, methods=["GET"])

    # Ruta Listado de usuarios por paginas
    # app.add_url_rule("/usuarios/page/<int:page>",
    #                 "usuario_listado", usuario.listado)

    # Ruta Busqueda de usuarios
    app.add_url_rule("/listausuarios", "usuario_listado", usuario.listado)
    app.add_url_rule("/listausuarios", "busqueda_usuarios",
                     usuario.busqueda, methods=["POST"])

    # Ruta para Roles
    app.add_url_rule("/roles", "rol_index", rol.index)
    app.add_url_rule("/roles", "rol_create", rol.create, methods=["POST"])

    # Rutas Centros
    app.add_url_rule("/listado_centros", "listado_centros", centro.listado)
    app.add_url_rule("/listado_centros", "busqueda_centros", centro.busqueda, methods=["POST"])
    app.add_url_rule("/listado_descarga/<path:filename>", "listado_descarga",
                     centro.downloadFile, methods=["GET"])
    app.add_url_rule("/nuevo-centro", "centro_nuevo",
                     centro.nuevo_centro, methods=["GET"])
    app.add_url_rule("/nuevo-centro", "centro_create",
                     centro.create, methods=["POST"])
    app.add_url_rule("/listado_centros/eliminar_centro/<int:id>",
                     "centro_eliminar", centro.delete)
    app.add_url_rule("/listado_centros/modificarEstadoCentro/<int:id>",
                     "centro_toogle", centro.toogleState)
    app.add_url_rule("/listado_centros/editarCentro/<int:id>",
                     "centro_editar", centro.edit)

    app.add_url_rule("/listado_centros/administrarCentro",
                     "centro_manage", centro.manageState)

    app.add_url_rule("/listado_centros/guardarEdicion/<int:id>",
                     "centro_guardar_edicion", centro.guardarEdicion, methods=["POST"])

    app.add_url_rule("/listado_centros/aceptar/<int:id>",
                     "centro_aceptar", centro.aceptarCargaCentro)
    app.add_url_rule("/listado_centros/rechazar/<int:id>",
                     "centro_rechazar", centro.rechazarCargaCentro)

    # Rutas Configuracion de Sitio Web
    app.add_url_rule("/configuracionSitio",
                     "configuracion_sitio", sitio.configSitio)
    app.add_url_rule("/configuracionSitio", "configuracion_sitio_guardar",
                     sitio.actualizarInfo, methods=["POST"])

    app.add_url_rule("/modificarEstadoSitio",
                     "sitio_modificarHabilitacion", sitio.modificarHabilitacion)

    app.add_url_rule("/modificarEstadoSitio",
                     "sitio_modificarHabilitacion", sitio.modificarHabilitacion)

    # Rutas turnos
    app.add_url_rule("/sacarTurno/<int:idCentro>","formTurno",turno.cargarForm, methods=["GET"])
    app.add_url_rule("/sacarTurno","turno_nuevo",turno.nuevo_turno, methods=["POST"])
    app.add_url_rule("/centros/<int:idCentro>/turnos","centro_turnos",turno.turnos_de_centro, methods=["GET"])
    app.add_url_rule("/eliminarTurno","eliminar_turno",turno.eliminarTurno, methods=["GET"])

    #Ruta para API turnos
    app.add_url_rule ("/centros/<int:idCentro>/turnos_disponibles/", "getTurnosPorFechaAPI", turno.getTurnosAPI, methods=["GET"])
    app.add_url_rule ("/centros/<int:idCentro>/reservas", "setReservaDeTurnoAPI", turno.setReservaAPI, methods=["POST"])

    @app.errorhandler(InternalServer)
    def handle_object_not_found_error(e):
        return jsonify({'message': str(e)}), 500

    @app.errorhandler(BadRequest)
    def handle_object_not_found_error(e):
        return jsonify({'message': str(e)}), 400

    # Ruta para el Home
    def home():
        if not 'id' in session:
            return redirect(url_for("usuario_login"))
        return redirect(url_for("listado_centros"))
    app.add_url_rule("/", "home", home)
    app.add_url_rule("/centros","centros_get",centro.getCentrosApi,methods=["GET"])
    app.add_url_rule("/centros/<int:centro_id>","centros_id",centro.getCentrosIdApi,methods=["GET"])
    app.add_url_rule("/centros","centros_post",centro.postCentrosApi,methods=["POST"])
    
    # @app.route("/webprivada")
    # def webprivada():
    #    if 'id' in session:
    #        return render_template("base.html", id=session["id"])
    #    return redirect(url_for("usuario_login"))

    # Rutas de API-rest
    #app.add_url_rule("/api/consultas", "api_issue_index", api_issue.index)

    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    # Implementar lo mismo para el error 500 y 401

    # Retornar la instancia de app configurada

    return app
