import json
import flask
from flask import redirect, render_template, make_response
from flask_login import current_user

from data import db_session
from data.models.classes import Classes
from data.models.users import User
from forms.class_form import ClassForm

blueprint = flask.Blueprint(
    'classes_function',
    __name__,
    template_folder='templates'
)

with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)


@blueprint.route('/class_create', methods=['POST', 'GET'])
def class_create():
    if not current_user.is_authenticated:
        return redirect('/login')
    if not current_user.is_confirm:
        return redirect('/')
    form = ClassForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        classes = Classes()
        classes.title = form.title.data
        classes.about = form.about.data
        classes.id_owner = current_user.id
        db_sess.add(classes)
        db_sess.commit()
        return redirect('/')
    return render_template('basic/class_form.html', form=form, title='Создание класса')


@blueprint.route('/class_edit/<int:id_class>', methods=['POST', 'GET'])
def class_edit(id_class):
    if not current_user.is_authenticated:
        return redirect('/login')
    db_sess = db_session.create_session()
    classes = db_sess.query(Classes).get(id_class)
    if not classes:
        return make_response(404)
    if current_user.id != classes.id_owner:
        return redirect('/')
    form = ClassForm()
    if form.validate_on_submit():
        classes.title = form.title.data
        classes.about = form.about.data
        classes.id_owner = current_user.id
        db_sess.add(classes)
        db_sess.commit()
        return redirect('/')
    form.title.data = classes.title
    form.about.data = classes.about
    return render_template('basic/class_form.html', form=form, title='Создание класса')


@blueprint.route('/class_delete/<int:id_class>', methods=['POST', 'GET'])
def class_delete(id_class):
    if not current_user.is_authenticated:
        return redirect('/login')
    db_sess = db_session.create_session()
    classes = db_sess.query(Classes).get(id_class)
    if not classes:
        return make_response(404)
    if current_user.id != classes.id_owner:
        return redirect('/')
    db_sess.delete(classes)
    db_sess.commit()
    return redirect('/')