import json
import flask
from flask import redirect, render_template, make_response, render_template_string, abort
from flask_login import current_user
from flask_mailman import EmailMessage
from data import db_session
from data.models.classes import Classes
from data.models.relation_model import RelationUserToClass
from forms.feadbacks import FeadBack
from static.message.feadback_template import feadback_template

import flask_login

blueprint = flask.Blueprint(
    'feadback_function',
    __name__,
    template_folder='templates'
)

with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)


@blueprint.route('/feadback', methods=['GET', 'POST'])
@flask_login.login_required
def feadback():
    if not current_user.is_authenticated:
        return redirect("/index")

    form = FeadBack()
    if form.validate_on_submit():
        email_body = render_template_string(feadback_template,
                                            text=form.text.data,
                                            email=current_user.email,
                                            name=current_user.name)
        # отправляем письмо администратору
        message = EmailMessage(
            subject=form.title.data,
            body=email_body,
            to=['journal1234coop@gmail.com']
        )
        message.content_subtype = "html"

        message.send()
        return redirect('/')
    return render_template('basic/feadback.html', form=form)


@blueprint.route('/feadback/<int:class_id>', methods=['GET', 'POST'])
@flask_login.login_required
def feadback_by_teacher(class_id):
    if not current_user.is_authenticated:
        return redirect("/index")

    form = FeadBack()
    db_sess = db_session.create_session()
    if db_sess.query(RelationUserToClass).filter(RelationUserToClass.id_class == class_id,
                                                 current_user.id == RelationUserToClass.id_user).first():
        if form.validate_on_submit():
            email_body = render_template_string(feadback_template,
                                                text=form.text.data,
                                                email=current_user.email,
                                                name=current_user.name)
            # отправляем письмо учителю от ученика
            message = EmailMessage(
                subject=form.title.data,
                body=email_body,
                to=[db_sess.query(Classes).filter(Classes.id == class_id).first().owner.email]
            )
            message.content_subtype = "html"

            message.send()
            return redirect('/')
        return render_template('basic/feadback.html', form=form)
    else:
        return abort(403)
