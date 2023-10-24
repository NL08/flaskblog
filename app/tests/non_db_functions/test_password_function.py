import pytest

# working forms return None

@pytest.fixture
def plaintext_password_contains_capital_form():
    password_form = 'efhwpaihrAf'
    return password_form

@pytest.fixture
def plaintext_password_form_contains_number():
    password_form = 'foelkjmf2'
    return password_form

@pytest.fixture
def plaintext_password_form_contains_special_char():
    password_form ='oejfpwo;fkjeo;'
    return password_form

 
# forms return redirect in the function this is when something has gone wrong

@pytest.fixture
def plaintext_password_form_not_contains_capital():
    password_form = 'ffffffffffff'
    return password_form

@pytest.fixture
def plaintext_password_form_not_contains_number():
    password_form = 'ffffffffff'
    return password_form

@pytest.fixture
def plaintext_password_form_not_contains_special_char():
    password_form = 'ffffffffff'
    return password_form

 




from flask import redirect, url_for


# test redirects
#def redirect_function():
#    return redirect(url_for('auth.register'))
#import sys

#from app.auth.functions import check_if_username_or_email_is_in_db



from app.auth.functions import make_password_contain_capital
from wsgi import app

from app.auth.forms import LoginForm
from wtforms.validators import ValidationError


#def test_password_1(yield_nonexistent_form):
#    with app.test_request_context():
        
#        with pytest.raises(ValidationError):
#            form = LoginForm()
#            field = yield_nonexistent_form 
#            make_password_contain_capital(form, field)







        # The functions here should return None     
        #assert make_password_contain_capital(plaintext_password_form_contains_capital) == None
        #assert make_password_contain_number(plaintext_password_form_contains_number) ==  None
        #assert make_password_contain_special_characters(plaintext_password_form_contains_special_char) ==  None
    


#def test_password_2(plaintext_password_form_not_contains_capital, plaintext_password_form_not_contains_number,
#    plaintext_password_form_not_contains_special_char):
    




#    with app.test_request_context():   
#        print(make_password_contain_capital(plaintext_password_form_not_contains_capital))



        # The functions here should return redirect
        
        # shortening the functions 
        # all these functions should fail
#        make_password_not_contain_capital = make_password_contain_capital(plaintext_password_form_not_contains_capital) 
#        make_password_not_contain_number = make_password_contain_number(plaintext_password_form_not_contains_number) 
#        make_password_not_contain_special_characters = make_password_contain_special_characters(plaintext_password_form_not_contains_special_char) 
        


        # making redirect functions work by printing not sure how print works
#        testing_redirect_function = sys.stdout.write(str(redirect_function()))
        


#        redirect_function_1 = sys.stdout.write(str(make_password_not_contain_capital))
#        redirect_function_2 = sys.stdout.write(str(make_password_not_contain_number))
#        redirect_function_3 = sys.stdout.write(str(make_password_not_contain_special_characters))

        # both functions in the assert should return redirect
#        assert testing_redirect_function == redirect_function_1 
#        assert testing_redirect_function == redirect_function_2 
#        assert testing_redirect_function == redirect_function_3 

# register
'''
make_password_contain_a_number
make_password_contain_a_capital
make_password_contain_special_characters 
compare_registration_password_fields
'''