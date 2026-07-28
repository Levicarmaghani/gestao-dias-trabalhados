from flask import flash, redirect, render_template, url_for
from flask_login import login_user, current_user, logout_user, login_required

from app.forms.cadastro_form import UserForm
from app.forms.login_form import LoginForm
from app.views import main_bp
from app import bcrypt

from app.models.cadastro_usuario import User




#============================
# LOGIN USUARIO
#=============================

@main_bp.route('/', methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('main.registro_dias'))
    
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
        usuario = form.save()

        login_user(usuario)
        flash("Cadastro efetuado com sucesso!", "success")
        return redirect(url_for('main.registro_dias'))

    return render_template(
        'cadastro.html',
        form=form
    )

# ==========================
#       LOGOUT
# ==========================
@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta", 'info')
    return redirect(url_for('main.login'))
    
        