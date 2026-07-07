from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Optional, Email, EqualTo, ValidationError

from app import db, bcrypt
from app.models.registro_dias import  RegistroTrabalho

#=====================  Registro de Trabalho=============
class RegistroForm (FlaskForm):
    data = DateField('Data', validators=[DataRequired()])
    local = StringField('Local', validators=[DataRequired()])
    valor = FloatField('Valor R$', validators=[DataRequired()])
    submit = SubmitField('Salvar')
    pesquisar = StringField("", render_kw={'placeholder':'Digite o local ou a data para pesquisar'})
    buscar= SubmitField('Pesquisar')

    def save(self):
        registro = RegistroTrabalho(
            data = self.data.data,
            local = self.local.data,
            valor = self.valor.data,
            )
        db.session.add(registro)
        db.session.commit()
        return registro