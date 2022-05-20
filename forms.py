from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional
from flask_wtf import FlaskForm

class Register(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    email = StringField("Email")
    first_name = StringField("First Name")
    last_name = StringField("Last Name")

class Login(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")


class FeedbackForm(FlaskForm):
    title = StringField("Title")
    content = StringField("Content")


class DeleteForm(FlaskForm):
    """Delete form -- this form is intentionally blank."""