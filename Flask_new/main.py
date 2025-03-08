from flask import Flask, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

app= Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class LoginForm(FlaskForm):
    astro_name = StringField('Id астронавта', validators=[DataRequired()])
    astro_password = PasswordField('Пароль астронавта', validators=[DataRequired()])

    cap_name = StringField('Id капитана', validators=[DataRequired()])
    cap_password = PasswordField('Пароль капитана', validators=[DataRequired()])

    submit = SubmitField('Войти')

@app.route('/')
def base():
    return render_template('base.html')
    
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        print('все норм')
        return redirect('/success')
    print('все плохо')
    return render_template('index.html', title='Авторизация', form=form)

@app.route('/success')
def success():
    return "Регистрация прошла успешно !!!"

if __name__ == '__main__':
    app.run(debug=True)