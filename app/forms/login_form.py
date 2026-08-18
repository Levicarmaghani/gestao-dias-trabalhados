from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

from app import bcrypt
from app.models.cadastro_usuario import User


class LoginForm(FlaskForm):
    email = EmailField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

    def autenticar(self):
        usuario = User.query.filter_by(email=self.email.data).first()

        if not usuario:
            return None

        if not bcrypt.check_password_hash(usuario.senha, self.senha.data):
            return None

        return usuario 