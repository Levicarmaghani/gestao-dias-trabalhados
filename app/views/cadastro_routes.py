from flask import flash, redirect, render_template, url_for
from flask_login import login_user

from app.forms.cadastro_form import UserForm
from app.forms.login_form import LoginForm
from app.views import main_bp
from app import bcrypt

from app.models.cadastro_usuario import User




from app.views import main_bp
#============================
# LOGIN USUARIO
#=============================

@main_bp.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        usuario = User.query.filter_by(email=form.email.data).first()

        if usuario and bcrypt.check_password_hash(usuario.senha, form.senha.data):
            login_user(usuario)
            # Retornando a função da rota do arquivo (registro_dias)
            return redirect(url_for('main.registro_dias'))
        
        flash('E-mail ou senha incorretos', 'danger')

    return render_template('login.html', form=form)


# ==========================
# CADASTRO DE USUÁRIO
# ==========================

@main_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro_usuario():

    form = UserForm()

    if form.validate_on_submit():
        form.save()

        flash("Cadastro efetuado com sucesso!", "succes")
        return redirect(url_for('main.login'))

    return render_template(
        'cadastro.html',
        form=form
    )

    
        