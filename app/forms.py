from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, RadioField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class NewDeviceForm(FlaskForm):
    device = StringField('Device name', validators=[DataRequired()])
    mode = RadioField('Mode',
        choices = [('all','all'), ('whitelist', 'whitelist')],
        default = 'all',
        validators = [DataRequired()])
    submit = SubmitField('Add')

class SetDeviceForm(FlaskForm):
    device = StringField('Device name', validators=[DataRequired()])
    mode = RadioField('Mode',
        choices = [('all','all'), ('whitelist', 'whitelist')],
        default = 'all',
        validators = [DataRequired()])
    submit = SubmitField('Set')

class DeleteDeviceForm(FlaskForm):
    device = StringField('Device name', validators=[DataRequired()])
    submit = SubmitField('Remove')

class AuthorizeForm(FlaskForm):
    username = StringField('Username')
    device = StringField('Device')
    submit = SubmitField('Confirm')
