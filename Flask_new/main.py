from flask import Flask, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField,  IntegerField 
from wtforms.validators import DataRequired

app= Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class LoginForm(FlaskForm):
    astro_name = StringField('Id астронавта', validators=[DataRequired()])
    astro_password = PasswordField('Пароль астронавта', validators=[DataRequired()])

    cap_name = StringField('Id капитана', validators=[DataRequired()])
    cap_password = PasswordField('Пароль капитана', validators=[DataRequired()])

    submit = SubmitField('Войти')


class Person(FlaskForm):
    name = StringField('Введите имя', validators=[DataRequired()])
    age =  IntegerField ('Введите возраст', validators=[DataRequired()])
    sex = SelectField('Ваш пол:', choices=[('man', 'Мужской'), ('woman', 'Женский')], validators=[DataRequired()])
    submit = SubmitField('Получить каюту')

@app.route('/base')
def base():
    return render_template('base.html')
    
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('index.html', title='Авторизация', form=form)

@app.route('/success')
def success():
    return "Регистрация прошла успешно !!!"

@app.route('/distribution')
def distribution():
    workers = ['Ридли Скотт', 'Энди Уир', 'Марк Уонти', 'Венката Капур', 'Тедди Сандерс', 'Шон Бин']
    return render_template('distribution.html', workers=workers)

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Person()
    if form.validate_on_submit():
        return redirect(f'/table/{form.sex.data}/{form.age.data}')
    
    return render_template('login.html', form=form)
    
@app.route('/table/<sex>/<age>')
def table(sex, age):
    return render_template('table.html', sex=sex, age=int(age))



if __name__ == '__main__':
    app.run(debug=True)
