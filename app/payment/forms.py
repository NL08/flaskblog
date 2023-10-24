# Register forms 
from flask_wtf import FlaskForm
from wtforms import DecimalField, validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, ValidationError


class EmptyForm(FlaskForm):
    pass 


class EmailForm(FlaskForm):
    
    email = EmailField('Email', validators=
    [
    DataRequired('Email is required'),
    # Is the line below useful
    Length(min=4, max=25, message='Must be between 4 and 25 characters'),
    ])

