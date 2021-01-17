from flask import request, render_template, url_for, redirect, flash, session, abort, jsonify
from app.models.turno import Turno
from app.resources import centro,sitio,usuario
from sqlalchemy import or_
from app.db_sqlalchemy import db_sqlalchemy
from app.helpers.auth import authenticated
from datetime import datetime,timedelta
from app.helpers.autsitio import sitioHabilitado
from app.factory.turnoFactory import TurnoFactory
from app.factory.reservaFactory import ReservaFactory
from app.resources.error_handling import InternalServer, BadRequest
import traceback

def verificarSesion():
    if not authenticated(session):
        abort(401)

def all():
    return Turno.all()

def cargarForm(idCentro):
    fechaHoy= datetime.now()
    one_day = timedelta(days=1)
    fechaMañana= fechaHoy + one_day
    fechaPasado= fechaMañana + one_day
    
    fechas=[fechaHoy.date(),fechaMañana.date(),fechaPasado.date()]

    horas=[]
    horas.append(datetime.strptime("09:00","%H:%M"))
    horas.append(datetime.strptime("09:30","%H:%M"))
    for each in range(10,16):
        horas.append(datetime.strptime((str(each)+":00"),"%H:%M"))
        horas.append(datetime.strptime((str(each)+":30"),"%H:%M"))
    horas.append(datetime.strptime("16:00","%H:%M"))

    elCentro= centro.buscarPorId(idCentro)
    turnos=armarTurnos(fechas,horas)
    turnosNuevos= quitarOcupados(turnos,elCentro.turnos)

    turnosNuevosStr=[]
    for each in turnosNuevos:
        fechaT=each.fecha.strftime("%Y-%m-%d")
        horaT=each.hora_inicio.strftime("%H:%M")
        turnosNuevosStr.append(fechaT + "   -   " + horaT)

    return render_template("sacarTurno.html",turnos=turnosNuevosStr,centro=elCentro)

def armarTurnos(fechas,horas):
    resul=[]
    for each in fechas:
        for each2 in horas:
            turno=Turno("",each,each2,"","","")
            resul.append(turno)
    return resul

def quitarOcupados(turnos,turnos_del_centro):
    resul=turnos
    for each in turnos_del_centro:
        if(each.enabled==1) and (datetime.now().date() <=each.fecha):
            for each2 in resul:
                if each2.fecha==each.fecha and each2.hora_inicio.time()==each.hora_inicio:
                    resul.remove(each2)
    return resul
    
def nuevo_turno():
    datos = request.form
    email = datos["email"].strip()
    turno = datos["turno"]
    telefono = datos["telefono"].strip()
    elCentro = centro.buscarPorId(int(request.args.get("idCentro")))
    if(len(turno)!=18):
        print("LEN: " + str(len(turno)))
        flash("Fecha u Horario invalidos, proba de nuevo","error")
        return redirect(url_for("formTurno",idCentro=elCentro.id))
    fecha = turno[0:10]
    
    fecha = datetime.strptime(fecha,"%Y-%m-%d")
    hora = turno[-5:]
    hora = datetime.strptime(hora,"%H:%M")
    print(fecha)
    print(hora)

    if verificarFecha(fecha) and verificarHora(hora):
        for each in elCentro.turnos:
            if each.enabled == 1:
                if each.fecha.strftime("%Y-%m-%d")==fecha.strftime("%Y-%m-%d") and each.hora_inicio.strftime("%H:%M")==hora.strftime("%H:%M"):
                    flash("Turno ya reservado! Por favor elegi otra fecha u horario","error")
                    return redirect (url_for("formTurno",idCentro=elCentro.id))
        if telefono == "":
            telefono="No Data"
        turno=Turno(email,fecha,hora, telefono)
        turno.save()
        elCentro.turnos.append(turno)
        elCentro.actualizar()
    else:
        flash("Fecha u Horario invalidos, proba de nuevo","error")
        return redirect(url_for("formTurno",idCentro=elCentro.id))
    flash("¡Turno cargado con exito!","success")
    return redirect(url_for("centro_turnos",idCentro=elCentro.id))

def verificarFecha(fecha):
    hoy= datetime.now()
    one_day = timedelta(days=1)
    fechaMañana= hoy + one_day
    fechaPasado= fechaMañana + one_day
    
    fechaHoy= hoy.strftime("%Y-%m-%d")
    fechaMañana= fechaMañana.strftime("%Y-%m-%d")
    fechaPasado= fechaPasado.strftime("%Y-%m-%d")
    
    if datetime.strftime(fecha,"%Y-%m-%d") == fechaHoy:
        return True
    else:
        if datetime.strftime(fecha,"%Y-%m-%d") == fechaMañana:
            return True
        else:
            if datetime.strftime(fecha,"%Y-%m-%d") == fechaPasado:
                return True
            else:
                print("LA FECHA ESTA MAL")
                return False

def verificarHora(hora):
    hora=hora.strftime("%H:%M")
    if hora == "09:00" or hora=="09:30":
        return True
    else:
        for each in range(10,16):
            horario=str(each) + ":"
            if (horario+"00")==hora or (horario+"30")==hora:
                return True
    if hora == "16:00": 
        return True
    print("LA HORA ESTA MAL")
    return False

def verificarRolOperador():
    usu= usuario.buscarPorId(session.get("id"))
    for each in usu.roles:
        if each.nombre=="Operador":
            return True
    return False


def turnos_de_centro(idCentro):
    if sitioHabilitado(session):
        verificarSesion()
        if(not verificarRolOperador()):
            flash("No tiene permiso para acceder a esta área","error")
            return redirect(url_for("listado_centros"))
        page = int(request.args.get('page', '1')) #numeroDePagina
        email = request.args.get('email', None) #selectAFiltrar (mail elegido)
        idCentro = int(idCentro)
        elCentro = centro.buscarPorId(idCentro)
        
        if email is not None:
            turnos=[]
            turnosTemp=elCentro.turnos
            for each in turnosTemp:
                if each.email_contacto == email and each.enabled==1:
                    turnos.append(each)    
        else:
            turnos=[]
            turnosTemp=elCentro.turnos
            for each in turnosTemp:
                if each.enabled==1:
                    turnos.append(each)    

        cant_elem = sitio.obtenerElementosPorPagina()

        fechaHoy= datetime.now()
        one_day = timedelta(days=1)
        fechaMañana= fechaHoy + one_day
        fechaPasado= fechaMañana + one_day
        
        fechaHoy= fechaHoy.strftime("%Y-%m-%d")
        fechaMañana= fechaMañana.strftime("%Y-%m-%d")
        fechaPasado= fechaPasado.strftime("%Y-%m-%d")

        turnosFinales=[]
       
        for each in turnos:
            if each.fecha.strftime("%Y-%m-%d")==fechaHoy:
                turnosFinales.append(each)
            else:
                if each.fecha.strftime("%Y-%m-%d")==fechaMañana:
                    turnosFinales.append(each)
                else:
                    if each.fecha.strftime("%Y-%m-%d")==fechaPasado:
                        turnosFinales.append(each)  

        turnosFinales= ordenarPorFechaYHora(turnosFinales)

        correos=[]
        for each in turnosFinales:
            if not correos.__contains__(each.email_contacto):
                correos.append(each.email_contacto)    
        correos.sort()
        
        pag_dic = paginarTurnos(turnosFinales,cant_elem,page)
        print(pag_dic)
        return render_template("turnosPorCentro.html", turnos=pag_dic["turnosF"], centro=elCentro, 
                                email=email, emailSelected=(email is not None),correos=correos, idCentro=idCentro,paginacion=pag_dic)
    else:
        if 'id' in session:
            del session['id']
        abort(401)


def paginarTurnos(turnos,cant_elem,page):
    cant_paginas = len(turnos) // cant_elem
    if(len(turnos)>cant_paginas*cant_elem):
        cant_paginas+=1

    has_prev=(page>1)
    has_next=(page<cant_paginas)
    prev_page=page-1
    next_page=page+1
    pages=range(1,cant_paginas+1)
    page=page

    pos=cant_elem*(page-1)
    turnosF=turnos[pos:(pos+cant_elem)]
    ret={
        "has_prev":has_prev,
        "has_next":has_next,
        "prev_page":prev_page,
        "next_page":next_page,
        "pages":pages,
        "page":page,
        "turnosF":turnosF,
        "hay_turnos":len(turnosF)>0}
    
    return ret

def eliminarTurno():
    idCentro = int(request.args.get('idCentro'))
    idTurno = int(request.args.get('idTurno'))
    Turno.eliminarPorId(idTurno)
    flash("¡Turno eliminado con exito!","success")
    return redirect(url_for("centro_turnos",idCentro=idCentro))

def ordenarPorFechaYHora(turnos):
    izquierda = []
    derecha = []
    if len(turnos) > 1:
        pivote = turnos[0]
        for i in turnos:
            if i != pivote:
                if i.fecha < pivote.fecha:
                    izquierda.append(i)
                elif i.fecha == pivote.fecha:
                    if i.hora_inicio < pivote.hora_inicio:
                        izquierda.append(i)
                    else:
                        derecha.append(i)
                elif i.fecha > pivote.fecha:
                    derecha.append(i)
        return ordenarPorFechaYHora(izquierda)+[pivote]+ordenarPorFechaYHora(derecha)
    else:
      return turnos

def turnos_API_por_fecha(idCentro,fecha):
    elCentro = centro.buscarPorId(idCentro)
    if (elCentro is None) or (elCentro.enabled == 0) or (elCentro.disponible != 1):
        return None
    turnos = elCentro.turnos

    horas=[]
    horas.append(datetime.strptime("09:00","%H:%M"))
    horas.append(datetime.strptime("09:30","%H:%M"))
    for each in range(10,16):
        horas.append(datetime.strptime((str(each)+":00"),"%H:%M"))
        horas.append(datetime.strptime((str(each)+":30"),"%H:%M"))
    horas.append(datetime.strptime("16:00","%H:%M"))

    turnosTotales = armarTurnos([fecha.date()],horas)
    
    turnosTotales = quitarOcupados(turnosTotales,turnos)

    return turnosTotales

def nuevo_turno_API (idCentro, nombre, apellido, email, telefono, hora_inicio, fecha):
    elCentro = centro.buscarPorId(idCentro)
    if (elCentro is None) or (elCentro.enabled == 0) or (elCentro.disponible != 1):
        return False
    for each in elCentro.turnos:
        if each.fecha.strftime("%Y-%m-%d")==fecha.date().strftime("%Y-%m-%d") and each.hora_inicio.strftime("%H:%M")==hora_inicio.time().strftime("%H:%M"):
            return None
    if telefono == "":
        telefono="No Data"
    turno=Turno(email,fecha,hora_inicio, telefono, nombre, apellido)
    turno.save()
    elCentro.turnos.append(turno)
    elCentro.actualizar()
    
    return turno

def getTurnosAPI (idCentro):
    try:
        fechaHoy = datetime.now().strftime("%Y-%m-%d")
        fecha_query = (request.args.get("fecha",fechaHoy))
        try: 
            fecha_queryOBJ = datetime.strptime(fecha_query, "%Y-%m-%d")  
        except:
            return jsonify({"message" : "Formato de fecha invalido"}), 500
        all_turns = turnos_API_por_fecha(idCentro,fecha_queryOBJ)
        if (all_turns is None):
            return jsonify({'message':'¡Error! idCentro en URL invalido'})
        turnos = []
        for each in all_turns:
            horaInicio = each.hora_inicio.time()
            horaFin = each.hora_fin.time()
            turnoFactory = TurnoFactory (idCentro, each.fecha, horaInicio, horaFin)      
            turnos.append(turnoFactory.serializar())
        return jsonify(Turnos_Disponibles=turnos),200
    except Exception:
        traceback.print_exc()
        raise InternalServer('Internal Server Error')

def setReservaAPI (idCentro):
    try:
        idCentroSTR = request.json["idCentro"]
        nombre = request.json["nombre"]
        apellido = request.json["apellido"]
        email_donante = request.json["email_donante"]
        telefono_donante = request.json["telefono_donante"]
        fechaSTR = request.json["fecha"]
        horaInicioSTR = request.json["horaInicio"]
        horaFinSTR = request.json["horaFin"]
        print (nombre)
        print (apellido)
        #### Dejar mas lindo para proxima entrega ###
        if (idCentroSTR is None):
            return jsonify({'message' : 'Por favor llenar campo: idCentro'}), 400
        if (nombre is None):
            return jsonify({'message: ' : 'Por favor llenar campo: nombre'})
        if (apellido is None):
            return jsonify({'message: ' : 'Por favor llenar campo: apellido'})
        if (email_donante is None):
            return jsonify({'message' : 'Por favor llenar campo: email_donante'}), 400
        if (fechaSTR is None):
            return jsonify({'message' : 'Por favor llenar campo: fecha'}), 400
        if (horaInicioSTR is None):
            return jsonify({'message' : 'Por favor llenar campo: hora_inicio'}), 400
        if (horaFinSTR is None):
            return jsonify({'message' : 'Por favor llenar campo: hora_fin'}), 400
        ###
        idCentroINT = int(idCentroSTR)
        if (idCentro != idCentroINT) : 
            return jsonify({'message' : 'Validacion de idCentro fallida'}), 400
        horaInicio = datetime.strptime(horaInicioSTR, "%H:%M")
        horaFin = datetime.strptime(horaFinSTR, "%H:%M")
        min = horaFin - horaInicio
        rango = timedelta(minutes=30)
        if (min != rango) :
            return jsonify({'message' : 'Bloque de turno incorrecto'}), 400
        try:
            fecha = datetime.strptime(fechaSTR, "%Y-%m-%d")  
        except:
            return jsonify({"message":"Formato de fecha invalido"}),400
        new_turno = nuevo_turno_API (idCentro, nombre, apellido, email_donante, telefono_donante, horaInicio, fecha)
        if (new_turno is False):
            return jsonify({'message' : '¡Error! idCentro en URL invalido'}), 500
        if (new_turno is None): 
            return jsonify({'message' : '¡Turno ocupado! Por favot elija un turno disponible'}), 400
        reservaFactory = ReservaFactory (idCentro, new_turno.nombre, new_turno.apellido, new_turno.email_contacto, new_turno.telefono_contacto, new_turno.fecha, new_turno.hora_inicio, new_turno.hora_fin) 
        return jsonify(reservaFactory.serializar()),201
    except Exception:
        traceback.print_exc()
        raise InternalServer('Internal Server Error')