# Importação de bibliotecas
from flask import render_template, redirect ,url_for, request, flash
from app.forms.dias_form import RegistroForm
from app.models.dia import RegistroTrabalho
from app import db
from sqlalchemy import func, or_


# Importando Blueprint
from app.views import main_bp

@main_bp.route('/', methods=['GET', 'POST'])
def home ():
    form = RegistroForm()

    if form.validate_on_submit():
        novo_registro = RegistroTrabalho(
            data = form.data.data,
            local = form.local.data,
            valor = form.valor.data
        )
        db.session.add(novo_registro)
        db.session.commit()

        flash('Registro salvo com sucesso!', 'info')
        return redirect(url_for('main.home'))

    registros = RegistroTrabalho.query.all()
    total = 0
    
    total_dias = len(registros)
    return render_template('index.html',  
        form=form,
        registros=registros,
        total = db.session.query(func.sum(RegistroTrabalho.valor)).scalar() or 0,
        total_dias=total_dias)


@main_bp.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    registro = RegistroTrabalho.query.get_or_404(id)

    db.session.delete(registro)
    db.session.commit()

    return redirect(url_for('main.home'))

@main_bp.route('/lista-dias')
def lista_dias():

    form = RegistroForm(request.args)    
    pesquisar = form.pesquisar.data or ""

    registros = RegistroTrabalho.query.order_by(RegistroTrabalho.data)

    if pesquisar != "":
        registros = registros.filter(or_(RegistroTrabalho.local.contains(pesquisar),
                                    RegistroTrabalho.data.contains(pesquisar)
                                    ))

    return render_template('index.html',
                            form = form,
                            registros = registros.all(),
                            pesquisar=pesquisar
                            )

      



@main_bp.route('/limpar')
def limpar_tabela():

    RegistroTrabalho.query.delete()
    db.session.commit()

    return redirect(url_for('main.home'))


