from app.db_sqlalchemy import db_sqlalchemy
from datetime import datetime
db = db_sqlalchemy


class Issue(db.Model):
    __tablename__ = 'issues'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    description = db.Column(db.Text())
    category_id = db.Column(db.Integer)
    status_id = db.Column(db.Integer)

    def __init__(self, email, descripcion, category_id, status_id):
        self.email = email
        self.description = descripcion
        self.category_id = category_id
        self.status_id = status_id

    def __repr__(self):
        return '<Issue {0} {1}: {2} {3}>'.format(self.email,
                                                 self.description,
                                                 self.category_id,
                                                 self.status_id)
