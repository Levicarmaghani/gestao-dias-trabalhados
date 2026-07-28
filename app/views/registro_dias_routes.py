from app import db
from sqlalchemy import func, or_
from flask_login import login_required, login_user


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

    registros = RegistroTrabalho.query.all()

    total_dias = len(registros)

    total = db.session.query(
        func.sum(RegistroTrabalho.valor)
    ).scalar() or 0

    return render_template(
        'registro_dias.html',
        form=form,
        registros=registros,
        total=total,
        total_dias=total_dias
    )


# ==========================
# EXCLUIR REGISTRO
# ==========================

@main_bp.route('/excluir/<int:id>', methods=['POST'])
@login_required
def excluir(id):

    registro = RegistroTrabalho.query.get_or_404(id)

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

    registros = RegistroTrabalho.query.order_by(
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

    return render_template('lista_dias.html',
        form=form,
        registros=registros,
        pesquisar=pesquisar,
        total=db.session.query(
            func.sum(RegistroTrabalho.valor)
        ).scalar() or 0,
        total_dias=RegistroTrabalho.query.count()
    )


# ==========================
# LIMPAR TABELA
# ==========================

@main_bp.route('/limpar')
@login_required
def limpar_tabela():

    RegistroTrabalho.query.delete()

    db.session.commit()

    return redirect(url_for('main.registro_dias'))