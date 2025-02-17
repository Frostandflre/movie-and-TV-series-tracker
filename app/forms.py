from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email

class RegistrationForm(FlaskForm):
    nickname = StringField('Nickname', [DataRequired()])
    email = StringField('Email', [DataRequired(), Email()])
    password = StringField('Password', [DataRequired()])
    submit = SubmitField('Подтвердить')

class AuthorizationForm(FlaskForm):
    email = StringField('Email', [DataRequired(), Email()])
    password = StringField('Password', [DataRequired()])
    submit = SubmitField('Войти')

class CommentForm(FlaskForm):
    comment = TextAreaField('Комментарий', [DataRequired()])
    submit = SubmitField('Отправить')
