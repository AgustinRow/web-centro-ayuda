from marshmallow import fields
from app.helpers.ext import ma
class CentroView(ma.Schema):

        nombre=fields.String(dump_only=True)
        direccion = fields.String()
        horario_apertura = fields.Time()
        horario_cierra = fields.Time()
        telefono=fields.String()
        tipo=fields.String()
        web=fields.String()
        email= fields.String()
        latitud = fields.Float()
        longitud = fields.Float()
        id= fields.Integer()
        municipio= fields.String()
