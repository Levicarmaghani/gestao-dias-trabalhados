from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

#================================================================================
#=========================== RECUPERAÇÃO DE SENHA ===============================
#================================================================================
class RecuperarSenhaForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    submit = SubmitField("recuperar senha")

#================================================================================
#=========================== REDEFINIR SENHA ====================================
#================================================================================
class RedefinirSenhaForm(FlaskForm):
    senha = PasswordField("Nova Senha", validators=[DataRequired(), Length(min=6)])
    confirmar_senha = PasswordField("Confirmar Senha", validators=[DataRequired(),
    EqualTo("senha", message="As senhas precisam ser iguais.")])
    submit = SubmitField("Redefinir senha")