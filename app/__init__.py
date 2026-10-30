# Importação de bibliotecas
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os 

# importando plataforma resend
import resend

# Carrega as variáveis de ambientes definidos no arquico .env
load_dotenv('.env')

#Recuperando chave secreta do .env
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
# configurando a API do resend, use a chave para autenticar minha aplicação
resend.api_key = RESEND_API_KEY


# Instância das extensões 
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()

# Factory da criação da apçicação Flask
def create_app():
    app = Flask(__name__)

    # Configuração da apçicação
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    #  Inicializações das extensões
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "main.login"
    bcrypt.init_app(app)

    # Registro dos blueprints
    from app.views import main_bp

    from app.models.cadastro_usuario import User, PasswordReset
    from app.models.registro_dias import RegistroTrabalho
    
    app.register_blueprint(main_bp)

    return app

