from flask import Flask, render_template, url_for, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField,  IntegerField, FileField
from wtforms.validators import DataRequired
import os
import json


app= Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'img', 'img_carousel')

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

class Load_Images(FlaskForm):
    file = FileField('Добавьте картинку', validators=[DataRequired()])
    submit = SubmitField('Загрузить')

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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Person()
    if form.validate_on_submit():
        return redirect(f'/table/{form.sex.data}/{form.age.data}')
    
    return render_template('login.html', form=form)
    
@app.route('/table/<sex>/<age>')
def table(sex, age):
    return render_template('table.html', sex=sex, age=int(age))


@app.route('/galery', methods=['GET', 'POST'])
def carousel():
    load = Load_Images()

    if request.method == 'POST':
        if load.validate_on_submit():
            f = load.file.data 
            filename = f.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename) # Формируем путь для сохранения
            f.save(file_path)

    lst_img = os.listdir(app.config['UPLOAD_FOLDER'])
    lst_img = [f'img/img_carousel/{x}' for x in lst_img]
    return render_template('carousel.html', lst_image=lst_img, form=load)

@app.route('/')
@app.route('/member')
def member():
     with open(os.path.join('templates', 'member.json'), encoding='utf-8') as file:
        data = json.load(file)  # Загружаем JSO
        persons = data["Persons"]
        return render_template('member.html', persons=persons)

if __name__ == '__main__':
    app.run(debug=True)
