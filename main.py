from flask import Flask, url_for, render_template, redirect
from forms.login_form import LoginForm
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'journalproject_secret_key'


def main():
    db_session.global_init("db/blogs.db")
    app.run()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Журнал')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


if __name__ == '__main__':
    main()
