
# ==========================
# IMPORTAÇÕES
# ==========================

from datetime import datetime, timedelta
import secrets

import resend

from flask import flash, redirect, render_template, url_for
from flask_login import (
    login_user,
    current_user,
    logout_user,
    login_required
)

from app import bcrypt, db
from app.views import main_bp

# Formulários
from app.forms.cadastro_form import UserForm
from app.forms.login_form import LoginForm
from app.forms.recuperar_senha_form import (RecuperarSenhaForm,RedefinirSenhaForm)

# Models
from app.models.cadastro_usuario import User, PasswordReset


# ==========================
# LOGIN DO USUÁRIO
# ==========================

@main_bp.route("/", methods=["GET", "POST"])
def login():

    # Se o usuário já estiver logado, vai direto para os registros
    if current_user.is_authenticated:
        return redirect(url_for("main.registro_dias"))

    form = LoginForm()

    # Valida o formulário e verifica o e-mail e a senha
    if form.validate_on_submit():

        usuario = form.autenticar()

        if usuario:
            login_user(usuario)

            # Redireciona para a rota de registro de dias
            return redirect(url_for("main.registro_dias"))

        flash("E-mail ou senha incorretos", "danger")

    return render_template("login.html", form=form)


# ==========================
# CADASTRO DE USUÁRIO
# ==========================

@main_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro_usuario():

    form = UserForm()

    if form.validate_on_submit():

        # Salva o novo usuário no banco de dados
        usuario = form.save()

        # Faz login automaticamente após o cadastro
        login_user(usuario)

        flash("Cadastro efetuado com sucesso!", "success")

        return redirect(url_for("main.registro_dias"))

    return render_template("cadastro.html",form=form)

# ==========================
# LOGOUT
# ==========================

@main_bp.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Você saiu da sua conta", "info")

    return redirect(url_for("main.login"))


# ==========================
# RECUPERAÇÃO DE SENHA
# ==========================

@main_bp.route("/esqueci_senha", methods=["GET", "POST"])
def esqueci_senha():

    form = RecuperarSenhaForm()

    if form.validate_on_submit():

        # Busca o usuário pelo e-mail informado no formulário
        usuario = User.query.filter_by(
            email=form.email.data
        ).first()

        if usuario:

            # Gera um token aleatório para a recuperação
            token = secrets.token_urlsafe(32)

            # Define o prazo de validade do token: 15 minutos
            expiracao = datetime.utcnow() + timedelta(minutes=15)

            # Cria o registro da recuperação de senha
            # O user_id liga essa recuperação ao usuário encontrado
            reset = PasswordReset(
                token=token,
                expiracao=expiracao,
                user_id=usuario.id
            )

            # Salva o registro no banco de dados
            db.session.add(reset)
            db.session.commit()

            # Gera o link com o token na URL
            link = url_for("main.recuperar_senha",token=token,_external=True)

            # Envia o e-mail com o link de recuperação
            resend.Emails.send({
                "from": "onboarding@resend.dev",
                "to": usuario.email,
                "subject": "Recuperação de senha",
                "html": f"""
                    <h2>Recuperação de senha</h2>

                    <p>
                        Clique no botão abaixo para redefinir sua senha:
                    </p>

                    <a href="{link}">
                        Redefinir minha senha
                    </a>

                    <p>
                        Este link é válido por 15 minutos.
                    </p>
                """
            })

            return redirect(url_for("main.email_enviado"))

        # Não revela se o e-mail está cadastrado
        # para evitar exposição de dados dos usuários
        flash(
            "Se o e-mail estiver cadastrado, você receberá um link.",
            "info"
        )

        return redirect(url_for("main.esqueci_senha"))

    return render_template("esqueci_senha.html",form=form)


# ==========================
# E-MAIL ENVIADO
# ==========================

@main_bp.route("/email_enviado")
def email_enviado():
    return render_template("email_enviado.html")


# ==========================
# REDEFINIÇÃO DE SENHA
# ==========================

@main_bp.route("/recuperar_senha/<token>", methods=["GET", "POST"])
def recuperar_senha(token):

    # Busca no banco o registro que possui o mesmo token
    # recebido pelo parâmetro da URL
    reset = PasswordReset.query.filter_by(token=token).first()

    # Verifica se o token existe no banco
    if not reset:
        return "Token inválido"

    # Verifica se o token já foi utilizado
    if reset.usado:
        return "Este token já foi utilizado"

    # Verifica se o prazo de validade do token expirou
    if datetime.utcnow() > reset.expiracao:
        return "Este token expirou"

    form = RedefinirSenhaForm()

    if form.validate_on_submit():

        # Busca o usuário pelo user_id da recuperação
        # O user_id faz a ligação entre PasswordReset e User
        usuario = User.query.get(reset.user_id)

        # Atualiza a senha do usuário com hash
        usuario.senha = bcrypt.generate_password_hash(
            form.senha.data
        ).decode("utf-8")

        # Marca o token como utilizado
        reset.usado = True

        # Salva a nova senha e a alteração do token
        db.session.commit()
        flash("Senha redefinida com sucesso!", "success")
        return redirect(url_for("main.login"))

    return render_template("redefinir_senha.html",form=form)