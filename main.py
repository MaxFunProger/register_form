from flask import Flask
from data import db_session
from data.users import *
from data.news import *
from flask import render_template
from register import RegisterForm
from flask import redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/register', methods=['GET', 'POST'])
def main():
    db_session.global_init('db/blogs.sqlite')
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register_form.html',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register_form.html',
                                   form=form,
                                   message="Такой колонист уже есть")
        user = User(
            address=form.address.data,
            speciality=form.speciality.data,
            position=form.position.data,
            age=form.age.data,
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/success')
    return render_template('register_form.html', form=form)


@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
