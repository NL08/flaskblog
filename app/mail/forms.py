# Register forms 
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, EqualTo, Length


class RequestResetPasswordForm(FlaskForm):
    '''
    This is in the /request_reset_password route
    The form is the email
    '''
    
    email = EmailField('Email', validators=
    [
    DataRequired('Email is required'),
    # Is the line below useful
    Length(min=4, max=25, message='Must be between 4 and 25 characters'),
    ])
    submit = SubmitField('Submit')   
 
class EmptyForm(FlaskForm):
    pass 


class ResetPasswordForm(FlaskForm):
    '''
    This is in the /reset_password/<token> route
    The forms are password and confirm_password
    '''
    

    password = PasswordField('Password', 
    [
        DataRequired('Email is required'),
        validators.Length(min=4, max=25),
        EqualTo('confirm_password', message='The password field is not equal to the confirm password field')
    ]) 
    submit = SubmitField('Submit')
 
    
    confirm_password = PasswordField('Password', 
    [
        DataRequired('Email is required'),
        validators.Length(min=4, max=25)
    ]) 
    submit = SubmitField('Submit')


     

