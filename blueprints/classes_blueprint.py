import json
import os

import flask
from flask import redirect, render_template, make_response
from flask_login import current_user
from data import db_session
from data.models.assessments import Assessments
from data.models.classes import Classes
from data.models.homework import Homework
from data.models.relation_model import RelationUserToClass
from data.models.users import User
from forms.class_form import ClassForm
from forms.class_join_form import ClassJoinForm
from forms.grade_form import GradeForm
from forms.home_work import HomeWork
from forms.status_class_privat import StatusPrivat
from tools.check_validate import check_validate_identifier
from tools.data_class_room import create_default_identifier, create_default_key
from tools.grade_analitycs import GPA

blueprint = flask.Blueprint(
    'classes_function',
    __name__,
    template_folder='templates'
)

with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)


@blueprint.route('/list_classes', methods=['POST', 'GET'])
def list_classes():
    if not current_user.is_authenticated:
        return redirect('/login')

    if not current_user.is_confirm:
        return redirect('/')

    # отображаем только те классы в которых состоит/управляет пользователь
    db_sess = db_session.create_session()
    classes_create = db_sess.query(Classes).filter(Classes.id_owner == current_user.id).all()[::-1]

    classes_join = db_sess.query(RelationUserToClass).filter(RelationUserToClass.id_user == current_user.id).all()[::-1]
    classes_join = [db_sess.query(Classes).filter(Classes.id == _.id_class).first() for _ in classes_join]

    return render_template('classes/list_classes.html',
                           title='Список классов',
                           classes_create=classes_create,
                           classes_join=classes_join)


@blueprint.route('/class_create', methods=['POST', 'GET'])
def class_create():
    if not current_user.is_authenticated:
        return redirect('/login')
    if not current_user.is_confirm:
        return redirect('/')

    form = ClassForm()
    if form.validate_on_submit():
        if form.title.data == '':
            return redirect('/class_create')

        db_sess = db_session.create_session()
        classes = Classes()
        classes.title = form.title.data
        classes.about = form.about.data
        classes.id_owner = current_user.id
        # если идентификатор не создан пользователем, то он создаётся автоматически
        if form.identifier.data == '':
            list_identifier = db_sess.query(Classes).filter(Classes.identifier).all()
            classes.identifier = create_default_identifier()
            while classes.identifier in list_identifier:
                classes.identifier = create_default_identifier()
        else:
            classes.identifier = form.identifier.data
            validity = check_validate_identifier(classes.identifier)
            if not validity:
                return render_template('classes/class_form.html',
                                       title='Создание класса',
                                       message='Идентификатор должен содержать только цифры',
                                       form=form)

        # если секретный ключ не создан пользователем, то он создаётся автоматически
        if form.secret_key.data == '':
            classes.secret_key = create_default_key()
        else:
            classes.secret_key = form.secret_key.data

        db_sess.add(classes)
        db_sess.commit()
        return redirect('/list_classes')

    return render_template('classes/class_form.html',
                           title='Создание класса',
                           form=form)


@blueprint.route('/class_join', methods=['POST', 'GET'])
def class_join():
    if not current_user.is_authenticated:
        return redirect('/login')
    if not current_user.is_confirm:
        return redirect('/')

    form_join = ClassJoinForm()
    if form_join.validate_on_submit():
        db_sess = db_session.create_session()
        classes = db_sess.query(Classes).filter(Classes.identifier == form_join.identifier.data).first()
        if classes:
            if classes.id_owner == current_user.id:
                return render_template('classes/class_join.html',
                                       form_join=form_join,
                                       message='Вы являетесь создателем класса',
                                       title='Вход в класс')

            elif db_sess.query(RelationUserToClass).filter(RelationUserToClass.id_class == classes.id,
                                                           RelationUserToClass.id_user == current_user.id).first():
                return render_template('classes/class_join.html',
                                       form_join=form_join,
                                       message='Вы уже состоите в этом классе',
                                       title='Вход в класс')

            elif classes.is_privat:
                return render_template('classes/class_join.html',
                                       form_join=form_join,
                                       message='Класс закрыт для присоединения',
                                       title='Вход в класс')

            elif classes.secret_key == form_join.secret_key.data:
                relation = RelationUserToClass()
                relation.id_class = classes.id
                relation.id_user = current_user.id
                db_sess.add(relation)
                db_sess.commit()
                return redirect('/list_classes')

            else:
                return render_template('classes/class_join.html',
                                       form_join=form_join,
                                       message='Неверный ключ доступа',
                                       title='Вход в класс')
        else:
            return render_template('classes/class_join.html',
                                   form_join=form_join,
                                   message='Неверный идентификатор',
                                   title='Вход в класс')

    return render_template('classes/class_join.html',
                           form_join=form_join,
                           title='Вход в класс')


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
    return render_template('classes/class_form.html', form=form, title='Редактирование класса')


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

    # если класс удалён, то удаляем все остальные записи связанные с этим классом
    relations = db_sess.query(RelationUserToClass).filter(RelationUserToClass.id_class == classes.id).all()
    for _ in relations:
        db_sess.delete(_)

    assessments = db_sess.query(Assessments).filter(Assessments.id_class == classes.id).all()
    for _ in assessments:
        db_sess.delete(_)

    home_work = db_sess.query(Homework).filter(Homework.id_class == classes.id).all()
    for _ in home_work:
        db_sess.delete(_)

    db_sess.delete(classes)
    db_sess.commit()

    return redirect('/list_classes')


@blueprint.route('/class/<int:id_class>', methods=['POST', 'GET'])
def classes(id_class):
    if not current_user.is_authenticated:
        return redirect('/login')

    db_sess = db_session.create_session()
    current_class = db_sess.query(Classes).filter(Classes.id == id_class).first()

    if current_user.id == current_class.id_owner:
        list_id_user, list_user = [], []
        for bunch in db_sess.query(RelationUserToClass).filter(RelationUserToClass.id_class == current_class.id).all():
            list_id_user.append(bunch.id_user)
        for user in db_sess.query(User).all():
            if user.id in list_id_user:
                list_user.append(user)

        form = StatusPrivat()
        if form.validate_on_submit():
            if current_class.is_privat:
                current_class.is_privat = 0
            else:
                current_class.is_privat = 1
            db_sess.commit()
            return redirect(f'/class/{id_class}')

        return render_template('/classes/class/class.html',
                               current_class=current_class,
                               users=list_user,
                               count_users=len(list_user),
                               form=form,
                               title=f'{current_class.title}')

    return redirect('/list_classes')


@blueprint.route('/class_user', methods=['POST', 'GET'])
def user_table_grade():
    if not current_user.is_authenticated:
        return redirect('/login')

    db_sess = db_session.create_session()

    # Получение всех связок: id_class - id_user
    all_class_user = db_sess.query(RelationUserToClass).filter(RelationUserToClass.id_user == current_user.id).all()

    # Словари вида: класс - данные из класса
    class_grade, class_gpa, class_titles = {}, {}, {}
    for bunch_class in all_class_user:
        user_grade, user_gpa = '', ''
        for bunch in db_sess.query(Assessments).filter(Assessments.id_class == bunch_class.id_class,
                                                       Assessments.id_student == bunch_class.id_user).all():
            user_grade += f'{bunch.value} '

        if not user_grade:
            user_grade = '—'
            user_gpa = '—'
        else:
            user_gpa = GPA(list(map(int, user_grade.rstrip().split())))
        class_grade[bunch_class.id_class] = user_grade
        class_gpa[bunch_class.id_class] = user_gpa

        class_titles[bunch_class.id_class] = db_sess.query(Classes).filter(
            Classes.id == bunch_class.id_class).first().title

    return render_template('/classes/class_user.html',
                           class_grade=class_grade,
                           class_titles=class_titles,
                           class_gpa=class_gpa,
                           title=f'Оценки')


@blueprint.route('/table_grade/<int:id_class>', methods=['POST', 'GET'])
def table_grade(id_class):
    if not current_user.is_authenticated:
        return redirect('/login')

    db_sess = db_session.create_session()
    current_class = db_sess.query(Classes).filter(Classes.id == id_class).first()

    if current_user.id != current_class.id_owner:
        return redirect('/list_classes')

    list_id_user, list_user = [], []
    for bunch in db_sess.query(RelationUserToClass).filter(RelationUserToClass.id_class == current_class.id).all():
        list_id_user.append(bunch.id_user)
    for user in db_sess.query(User).all():
        if user.id in list_id_user:
            list_user.append(user)

    dict_user_grade, dict_user_gpa = {}, {}
    for bunch in db_sess.query(Assessments).filter(Assessments.id_class == current_class.id).all():
        if bunch.id_student in dict_user_grade:
            dict_user_grade[bunch.id_student] += f'{bunch.value} '
        else:
            dict_user_grade[bunch.id_student] = f'{bunch.value} '
            dict_user_gpa[bunch.id_student] = ''

    for key, val in dict_user_grade.items():
        dict_user_gpa[key] = GPA(list(map(int, dict_user_grade[key].rstrip().split())))

    form = GradeForm()

    return render_template('/classes/class/table_grade.html',
                           form=form,
                           current_class=current_class,
                           users=list_user,
                           dict_user_grade=dict_user_grade,
                           dict_user_gpa=dict_user_gpa,
                           title=f'{current_class.title}')


@blueprint.route('/table_grade/<int:id_class>/<int:id_user>', methods=['POST', 'GET'])
def new_grade(id_class, id_user):
    db_sess = db_session.create_session()
    current_class = db_sess.query(Classes).filter(Classes.id == id_class).first()

    form = GradeForm()
    if form.validate_on_submit():
        assessment = Assessments()
        assessment.id_class = current_class.id
        assessment.id_student = id_user
        assessment.value = form.grade.data
        db_sess.add(assessment)
        db_sess.commit()
        return redirect(f'/table_grade/{id_class}')


@blueprint.route('/delete_user/<id_user>/<id_class>', methods=['POST', 'GET'])
def delite_user(id_user, id_class):
    db_sess = db_session.create_session()
    if current_user.id == db_sess.query(Classes).filter(Classes.id == id_class).first().id_owner:
        db_sess.query(RelationUserToClass).filter(RelationUserToClass.id_user == id_user,
                                                  RelationUserToClass.id_class == id_class).delete()
        db_sess.query(Assessments).filter(Assessments.id_class == id_class,
                                          Assessments.id_student == id_user).delete()
        db_sess.commit()

    return redirect(f'/class/{id_class}')


@blueprint.route('/create_home_work/<int:id_class>', methods=['POST', 'GET'])
def create_home_work(id_class):
    if not current_user.is_authenticated:
        return redirect('/login')

    db_sess = db_session.create_session()
    current_class = db_sess.query(Classes).filter(Classes.id == id_class).first()

    if current_user.id != current_class.id_owner:
        return redirect('/')

    form = HomeWork()
    choices = form.recipient.choices
    for bunch in db_sess.query(RelationUserToClass).filter(RelationUserToClass.id_class == id_class).all():
        choices.append((bunch.id_user,
                        f'''{db_sess.query(User).filter(User.id == bunch.id_user).first().name} 
                            {db_sess.query(User).filter(User.id == bunch.id_user).first().surname}'''))
    form.recipient.choices = choices

    if form.validate_on_submit():
        home_work = Homework()
        home_work.text = form.text.data
        home_work.date = form.date.data
        home_work.recipient = form.recipient.data
        home_work.id_class = current_class.id
        db_sess.add(home_work)
        db_sess.commit()
        if not os.path.exists('static/homework'):
            os.makedirs('static/homework')
        if form.file.data:
            homework = db_sess.query(Homework).filter(Homework.id == home_work.id).first()
            path_file = f'{homework.id}.{form.file.data.filename.split(".")[1]}'
            homework.file_name = path_file
            form.file.data.save(f'static/homework/{path_file}')
            db_sess.commit()

    return render_template('/classes/class/home_work.html',
                           form=form,
                           current_class=current_class,
                           title=f'Добавление домашнего задания')


@blueprint.route('/view_home_work', methods=['POST', 'GET'])
def view_home_work():
    if not current_user.is_authenticated:
        return redirect('/login')

    db_sess = db_session.create_session()
    # Получение всех связок: id_class - id_user
    all_class_user = db_sess.query(RelationUserToClass).filter(RelationUserToClass.id_user == current_user.id).all()
    class_titles = {}
    class_home_work = {}
    for bunch_class in all_class_user:
        class_titles[bunch_class.id_class] = db_sess.query(Classes).filter(
            Classes.id == bunch_class.id_class).first().title

        class_home_work[bunch_class.id_class] = db_sess.query(Homework).filter(
            Homework.id_class == bunch_class.id_class).all()

    return render_template('/classes/view_home_work.html',
                           class_titles=class_titles,
                           class_home_work=class_home_work,
                           title=f'Добавление домашнего задания')


@blueprint.route('/class_home_work/<int:id_class>', methods=['POST', 'GET'])
def class_home_work(id_class):
    if not current_user.is_authenticated:
        return redirect('/login')

    db_sess = db_session.create_session()
    if not db_sess.query(RelationUserToClass).filter(RelationUserToClass.id_class == Classes.id,
                                                     RelationUserToClass.id_user == current_user.id).first():
        return redirect('/list_classes')

    # Получение всех связок: id_class - id_user
    class_title = db_sess.query(Classes).filter(
        Classes.id == id_class).first().title

    class_home_works = db_sess.query(Homework).filter(
        Homework.id_class == id_class).all()[::-1]

    return render_template('/classes/class_home_work.html',
                           class_title=class_title,
                           class_home_works=class_home_works,
                           title=f'Просмотр домашнего задания')
