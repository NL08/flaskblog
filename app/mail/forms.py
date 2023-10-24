
# Register forms 
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, ValidationError


class RequestResetPasswordForm(FlaskForm):
    
    email = EmailField('Email', validators=
    [
    DataRequired('Email is required'),
    # Is the line below useful
    Length(min=4, max=25, message='Must be between 4 and 25 characters'),
    ])
       
 
class EmptyForm(FlaskForm):
    pass 


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', 
    [
        DataRequired('Email is required'),
        validators.Length(min=4, max=25)
    ]) 
    
    
    confirm_password = PasswordField('Password', 
    [
        DataRequired('Email is required'),
        validators.Length(min=4, max=25)
    ]) 
    

    '''
    # check if the email does not exist so you can throw an error 
    def validate (self, email):
        email = User.query.filter_by(email=email.data.first())
        # is None just checks if it is none
        if email is None: 
            raise ValidationError ("You have entered a email that does not exist. Please register a valid email.")
    ''' 

