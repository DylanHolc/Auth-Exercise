from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length
class AddUserForm(FlaskForm):
    first_name = StringField('First Name:', validators=[InputRequired(), Length(max=30)])
    last_name = StringField('Last Name:', validators=[InputRequired(), Length(max=30)])
    email = EmailField('Email:', validators=[InputRequired(), Length(max=50)])
    username = StringField('Username:', validators=[InputRequired(), Length(max=20)])
    password = PasswordField('Password:', validators=[InputRequired()])

class LoginUserForm(FlaskForm):
    username = StringField('Username:', validators=[InputRequired(), Length(max=20)])
    password = PasswordField('Password:', validators=[InputRequired()])

class AddFeedbackForm(FlaskForm):
    title = StringField('Title:', validators=[InputRequired(), Length(max=100)])
    content = StringField('Content:', validators=[InputRequired()])
