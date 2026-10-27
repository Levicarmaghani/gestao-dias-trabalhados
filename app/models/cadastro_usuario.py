from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
 
#=================================================================
# ======================REGISTRO USUÁRIO==========================
#=================================================================
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable = False)
    sobrenome = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    senha = db.Column(db.String(255), nullable = False)

    # Relação 1:N entre User e RegistroTrabalho
    registros_trabalho = db.relationship('RegistroTrabalho', backref = 'user', lazy=True)

#=======================================================================
#=========================RECUPERAÇÃO DE SENHA==========================
#========================================================================

class PasswordReset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), unique=True, nullable=False)
    expiracao = db.Column(db.DateTime, nullable=False)
    usado = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)