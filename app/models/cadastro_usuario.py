from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
 

# Registro Usuário
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable = False)
    sobrenome = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    senha = db.Column(db.String(255), nullable = False)
