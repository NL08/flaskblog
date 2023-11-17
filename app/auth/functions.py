# functions for routes.py 
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
         
    
import os

current_config = os.environ['FLASK_ENV']
# allow different imports so the code works during pytest + None pytest
if os.environ['FLASK_ENV']  == 'dev':
    from app.models import User  
elif os.environ['FLASK_ENV'] == 'test': 
    from app.tests.models import UserTest as User 
   
     
from app import db        

def check_if_username_not_in_db(form, field):    
    '''
    if the username is not in the db the code works,
    if not it raises an ValidationError.
    This runs in the RegistrationForm in  username column
    '''


    if db.session.execute(db.select(User).filter_by(username=field.data)).scalar_one_or_none():
        raise ValidationError('The username is already taken. Please select another username for registration.') # okay wording?  
    else: 
        print('Success the username is not taken and you can successfully register.')
        return 'success'


def check_if_email_not_in_db(form, field):    
    '''
    if the email is not in the db the code works,
    if not it raises an ValidationError.
    This runs in the RegistrationForm in auth/forms.py
    '''
    if db.session.execute(db.select(User).filter_by(email=field.data)).scalar_one_or_none():
        raise ValidationError('The email is already taken. Please select another username for registration.') # okay wording?  
    else: 
        print('Success the email is not taken and you can successfully register.')
        return 'success'
    
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
    if not db.session.execute(db.select(User).filter_by(username=field.data)).scalar_one_or_none() and not db.session.execute(db.select(User).filter_by(email=field.data)).scalar_one_or_none():
        raise ValidationError('The username or email or password do not exist. Please retype your username or email or password.')   
     
from argon2 import PasswordHasher

def compare_hashed_passwords(hashed_password_db, plaintext_password_form):
    '''   
    The code runs in the /login route.
    Compares the hashed_password in the db and plaintext password form.
    ph.verify(...) returns True if True and raises a validation error if False.  
    You don't want to raise a validation error in flask unless in wtf forms.
    '''
    ph = PasswordHasher()
    try:
        verified_hashed_password = ph.verify(hashed_password_db, plaintext_password_form)
        return verified_hashed_password
    except:
        return False


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

(Not a validator function)
compare_hashed_passwords
''' 
 





 