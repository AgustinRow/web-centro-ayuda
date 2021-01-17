from marshmallow import fields
from app.helpers.ext import ma

class TurnoView (ma.Schema):
    idCentro = fields.Integer()
    fecha = fields.String()
    horaInicio= fields.DateTime()
    horaFin = fields.DateTime()