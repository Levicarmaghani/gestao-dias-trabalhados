from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, SubmitField
from wtforms.validators import DataRequired, Optional

#Criando campo do html
class RegistroForm (FlaskForm):
    data = DateField('Data', validators=[DataRequired()])
    local = StringField('Local', validators=[DataRequired()])
    valor = FloatField('Valor R$', validators=[DataRequired()])
    salvar = SubmitField('Salvar')