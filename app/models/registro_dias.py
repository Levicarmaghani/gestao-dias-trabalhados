from app import db
from sqlalchemy import func

# Registro de dias
class RegistroTrabalho(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    local = db.Column(db.String(100), nullable=True)
    valor = db.Column(db.Float, nullable=False)

    @classmethod
    def valor_total(cls):
        total = db.session.query(func.sum(cls.valor)).scalar()

        if total is None:
            return 0
        
        return total


