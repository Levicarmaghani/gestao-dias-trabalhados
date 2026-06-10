# Importação bibliotecas
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Criação do banco 
db = SQLAlchemy()
migrate = Migrate()

# Configuração do banco de dados da aplicação
def create_app():
    app = Flask(__name__)

    # Conectando banco ao app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Chave usada para proteção de sessões e formulários
    app.config['SECRET_KEY'] = 'MGVÇKERGÇNERGPMP=-FNMPEW'

    db.init_app(app)
    migrate.init_app(app, db)

    # Importação de models
    from app.views.routes import main_bp
    app.register_blueprint(main_bp)

    return app

