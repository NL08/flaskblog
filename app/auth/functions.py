# functions for routes.py 
from flask import flash
from wtforms.validators import ValidationError

def make_password_contain_capital(form, field):
    '''
    This works if the password contains a capital Char 
    and raises an ValidationError if it does not.
    This runs in the class RegistrationForm in passwordfield + confirmpasswordfield column
    ''' 
    password_form = field.data   
    word = password_form
    # loops through each word into a char and if any char is an uppercase return True else return False
    letter = [char for char in word if char.isupper()]
    print(letter)
    # if the string returns True then the string has an capital  
    if letter: 
        print("Success password does contain a capital")
        return 'success'    
    else: 
        raise ValidationError("Please include a capital letter in the password field")  


def make_password_contain_number(form, field):
    '''
    This works if the password contains a number Char 
    and raises an ValidationError if it does not.
    This runs in the class RegistrationForm in passwordfield + confirmpasswordfield column
    '''  
    password_form = field.data   
    word = password_form
    # loops through each word into a char and if any char is an uppercase return True else return False
    letter = [char for char in word if char.isnumeric()]
    # if the string returns True then the string has an number   
    if letter:
        print("Success password does contain a number")  
        return 'success'   
    else: 
        raise ValidationError("Please include a number in the password field")
    

def make_password_contain_special_characters(form, field):
    '''
    This works if the password contains a special Char 
    and raises an ValidationError if it does not.
    This runs in the class RegistrationForm in passwordfield + confirmpasswordfield column
    '''
    password_form = field.data
    #print('field.data=',password_form)             
    password = password_form
    word = password    
    special_characters = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    # checks if char does have a special character
    boolean = [char for char in word if char in special_characters]
    # if the string returns a value then the string has an number  
    if boolean:
        print("Success password does contain a special character")
        return None
    # else executes if "letter" is an empyty string
    else:
      raise ValidationError("Please include a special character in the password field")
         
    
from app import app
# allow different imports so the code works during pytest + None pytest
if app.config['ENV'] == 'development':
    from app.models import User  
elif app.config['ENV'] == 'pytest': 
    from app.tests.models import UserTest as User 


def check_if_username_not_in_db(form, field):    
    '''
    if the username is not in the db the code works,
    if not it raises an ValidationError.
    This runs in the RegistrationForm in  username column
    '''

    if User.query.filter_by(username=field.data).first():
        raise ValidationError('The username is already taken. Please select another username for registration.') # okay wording?  
    else: 
        flash('Success the username is not taken and you can successfully register.')
        return None


def check_if_email_not_in_db(form, field):    
    '''
    if the email is not in the db the code works,
    if not it raises an ValidationError.
    This runs in the RegistrationForm in auth/forms.py
    '''
    if User.query.filter_by(email=field.data).first():
        raise ValidationError('The email is already taken. Please select another username for registration.') # okay wording?  
    else: 
        flash('Success the email is not taken and you can successfully register.')
        return None
    
# login functions
# Don't check passwords seperatly for security reasons!
def check_if_username_or_email_is_in_db(form, field):
    '''
    if the username or email is in the db the code works,
    if not it raises an ValidationError.
    The if statement checks if the query is empty/has no values in db.
    This runs in the LoginForm in auth/forms.py
    '''
  
 
    # if empty list [] return True 
    if not User.query.filter_by(username=field.data).first() and not User.query.filter_by(email=field.data).first(): 
        raise ValidationError('The username or email does not exist. Please retype your username or email.')   
     




# function list 
'''
(register functions)

make_password_contain_capital
make_password_contain_number
make_password_contain_special_characters

check_if_username_not_in_db
check_if_email_not_in_db

(login functions)
check_if_username_or_email_is_in_db
''' 
 





 