from app import db, bcrypt
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from wtforms import StringField, PasswordField, SubmitField

from flask_wtf import FlaskForm
from app.models.cadastro_usuario import User



#================ Classe cadastro m=======================
class UserForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired() ])
    sobrenome = StringField('Sobrenome ', validators=[DataRequired() ])
    email = StringField('E-mail', validators=[DataRequired(), Email() ])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmacao_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha', message='As senhas não coincidem') ])
    submit = SubmitField('Cadastrar')

    def validate_email(self, email):
        usuario = User.query.filter_by(email = email.data).first()
        if usuario:
            raise ValidationError("Usuário já cadastrado com esse E-mail")
    
    def save(self):
        senha_hash = bcrypt.generate_password_hash(self.senha.data).decode('utf-8')
        user = User(
            nome = self.nome.data,
            sobrenome = self.sobrenome.data,
            email = self.email.data,
            senha = senha_hash
        )
        db.session.add(user)
        db.session.commit()
        return user
