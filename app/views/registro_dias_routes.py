from app import db
from sqlalchemy import func, or_
from flask_login import login_required, login_user, current_user

from datetime import datetime


#  Importação biblioteca flask
from flask import render_template, redirect, url_for, request, flash

# Importação banco
from app.models.registro_dias import RegistroTrabalho

# Importação formulário
from app.forms.registro_dias_form import RegistroForm

# Importando Blueprint
from app.views import main_bp


# ==========================
# REGISTRO DE DIÁRIAS
# ==========================

@main_bp.route('/registro', methods=['GET', 'POST'])
@login_required
def registro_dias():

    form = RegistroForm()

    if form.validate_on_submit():
        form.save()

        flash("Registro salvo com sucesso!", "info")

        return redirect(url_for('main.registro_dias'))

    registros = RegistroTrabalho.query.filter_by(user_id=current_user.id).all()

    total_dias = len(registros)

    total = db.session.query(
        func.sum(RegistroTrabalho.valor)).filter(RegistroTrabalho.user_id == current_user.id).scalar() or 0

    return render_template(
        'registro_dias.html',
        form=form,
        registros=registros,
        total=total,
        total_dias=total_dias
    )
# ==========================
# Atividade Realizadas
# ==========================
@main_bp.route('/registro/<int:id>/atividades')
@login_required
def atividades(id):

    registro = RegistroTrabalho.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    form = RegistroForm(obj=registro)

    return render_template(
        'atividades.html',
        registro=registro,
        form=form
    )

# ==========================
# Editar atividades 
# ==========================

@main_bp.route('/editar/<int:id>/', methods=['GET', 'POST'])
@login_required
def editar_atividades(id):
    # Busca o registro do usuário logado 
    registro = RegistroTrabalho.query.filter_by(id=id, user_id=current_user.id).first_or_404()

    #Carrega os dados existentes no Formulário
    form = RegistroForm(obj=registro)

    #verifica se o formulário foi enviado
    if form.validate_on_submit():

        # Atualiza os campos 
        registro.data = form.data.data
        registro.local = form.local.data
        registro.valor = form.valor.data
        registro.atividade = form.atividade.data

        #Salva as alterações no banco de dados
        db.session.commit()

        # Volta para os detalhes da atividade
        return redirect(url_for('main.editar_atividades', id=registro.id))
    
    return render_template('atividades.html', form=form, registro=registro)
     



# ==========================
# EXCLUIR REGISTRO
# ==========================

@main_bp.route('/excluir/<int:id>', methods=['POST'])
@login_required
def excluir(id):

    registro = RegistroTrabalho.query.filter_by(id=id, user_id=current_user.id).first()

    if registro:
        db.session.delete(registro)
        db.session.commit()

    return redirect(url_for('main.registro_dias'))


# ==========================
# LISTA DE REGISTROS
# ==========================

@main_bp.route('/lista-dias')
@login_required
def lista_dias():

    form = RegistroForm(request.args)

    pesquisar = form.pesquisar.data or ""

    registros = RegistroTrabalho.query.filter_by(
        user_id=current_user.id
    ).order_by(
        RegistroTrabalho.data
    )

    if pesquisar != "":
        registros = registros.filter(
            or_(
                RegistroTrabalho.local.contains(pesquisar),
                RegistroTrabalho.data.contains(pesquisar)
            )
        )

    registros = registros.all()

    return render_template(
        'lista_dias.html',
        form=form,
        registros=registros,
        pesquisar=pesquisar,

        total=db.session.query(
            func.sum(RegistroTrabalho.valor)
        ).filter(
            RegistroTrabalho.user_id == current_user.id
        ).scalar() or 0,

        total_dias=RegistroTrabalho.query.filter_by(
            user_id=current_user.id
        ).count()
    )


# ==========================
# LIMPAR TABELA
# ==========================

@main_bp.route('/limpar', methods=['GET', 'POST'])
@login_required
def limpar_tabela():

    RegistroTrabalho.query.filter_by(
        user_id=current_user.id
    ).delete()

    db.session.commit()

    return redirect(url_for('main.registro_dias'))