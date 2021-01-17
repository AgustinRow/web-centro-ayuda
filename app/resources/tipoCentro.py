from app.models.tipoCentro import TipoCentro
from app.db_sqlalchemy import db_sqlalchemy


def all():
    return TipoCentro.all()
