# Register forms 
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import PasswordField, StringField, SubmitField  
from wtforms.fields.simple import FileField
from wtforms.validators import DataRequired, Length, EqualTo
from app.auth.functions import(check_if_username_not_in_db, check_if_email_not_in_db,
make_password_contain_capital, make_password_contain_number,
make_password_contain_special_characters)
 

class RegistrationForm(FlaskForm):
    '''
    This is in /register route.
    The forms are username, email, password and confirm_password
    '''
    username = StringField('username',validators=
    [
    DataRequired(message='Username is required'),
    Length(min=2, max=25 , message='Must be between 2 and 25 characters'),
    check_if_username_not_in_db
    ])  
    email = StringField('email', validators=
    [
    DataRequired('Email is required'),
    Length(min=4, max=35, message='Must be between 4 and 25 characters'),
    check_if_email_not_in_db
    ])
    password = PasswordField('password', 
    validators=
    [
    DataRequired('Password is required'), 
    Length(min=8, max=25, message='Must be between 8 and 25 characters'),
    EqualTo('confirm_password', message='The password field is not equal to the confirm password field'), 
    make_password_contain_capital,
    make_password_contain_number,
    make_password_contain_special_characters
    ])

    confirm_password = PasswordField('confirm_password',
    validators=
    [
    DataRequired('Does not match password'),
    make_password_contain_capital, 
    make_password_contain_number,
    make_password_contain_special_characters
    ])
    submit = SubmitField('Submit')

 
from app.auth.functions import check_if_username_or_email_is_in_db
class LoginForm(FlaskForm):
    '''
    This is in /Login route.
    The forms are username, email, password and confirm_password
    '''
    username_or_email = StringField('username_or_email', validators=
    [
    DataRequired(message='Please use Username or Email'), 
    Length(min=4, max=35 ,message='Must be between 4 and 25 characters'),
    check_if_username_or_email_is_in_db
    ])
    password = PasswordField('password', validators=
    [
    Length(min=8, max=25, message='Must be between 8 and 25 characters'),
    ])
    submit = SubmitField('Submit')
  

class UpdateAccountForm(FlaskForm):
    password = PasswordField('password', validators=
    [
    DataRequired(message='Password is required'), 
    Length(min=8, max=25, message='Must be between 8 and 25 characters'),
    ])
    confirm_password = PasswordField('Repeat Password', validators=
    [
    DataRequired(message='Does not match password')
    ])
    submit = SubmitField('Submit')

class EmptyForm(FlaskForm):
    '''This is in the /followers routes '''
    pass





# todo move later
class FileForm(FlaskForm): 
    '''
    This is in /update_form route.
    The form is image_filename.
    '''
    image_filename = FileField('image_filename', 
    validators=
    [FileRequired() ,FileAllowed(['jpg', 'png'], message='Images only!')  ])
    submit = SubmitField('Submit')



 
class SearchForm(FlaskForm):
    '''
    This is in the '/search' route.
    The form is searched.
    '''   
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")
