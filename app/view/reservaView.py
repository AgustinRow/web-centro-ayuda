from marshmallow import fields
from app.helpers.ext import ma

class ReservaView (ma.Schema):
    idCentro = fields.Integer()    
    nombre = fields.String()
    apellido = fields.String()
    email_donante = fields.String()
    telefono_donante = fields.String()
    fecha = fields.String()
    horaInicio = fields.DateTime()
    horaFin = fields.DateTime()