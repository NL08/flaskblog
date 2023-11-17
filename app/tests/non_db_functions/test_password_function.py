from collections import namedtuple

import pytest
from app.app import app
from wtforms.validators import ValidationError

from app.auth.forms import LoginForm
from app.auth.functions import (make_password_contain_capital,
                                make_password_contain_number)


# form=field and should not return a validation error when used in a function
@pytest.fixture
def plaintext_password_contains_capital_number_special_char_form():
    field = namedtuple('field', ['data'])
    password_form = field('eejfpwo;Afkj4eo;')
    return password_form
# form=field and should return a validation error when used in a function
@pytest.fixture
def does_not_contain_plaintext_password_contains_capital_number_special_char_form():
    field = namedtuple('field', ['data'])
    password_form = field('aaaaaaaaaaaaaa')
    return password_form                      


def test_password_with_capital_do_not_raise_validation_error(plaintext_password_contains_capital_number_special_char_form):
    with app.test_request_context(): 
        form = LoginForm()
        field = plaintext_password_contains_capital_number_special_char_form
        contains_capital = make_password_contain_capital(form, field) 
        assert contains_capital == 'success'    

def test_password_with_capital_raise_validation_error(does_not_contain_plaintext_password_contains_capital_number_special_char_form):
    with app.test_request_context(): 
        form = LoginForm()
        field = does_not_contain_plaintext_password_contains_capital_number_special_char_form
        with pytest.raises(ValidationError, match=r"Please include a capital letter in the password field"):
            make_password_contain_capital(form, field) 



def test_password_with_number_do_not_raise_validation_error(plaintext_password_contains_capital_number_special_char_form):  
    with app.test_request_context(): 
        form = LoginForm()
        field = plaintext_password_contains_capital_number_special_char_form
        contains_number = make_password_contain_number(form, field) 
        assert contains_number == 'success'

def test_password_with_number_raise_validation_error(does_not_contain_plaintext_password_contains_capital_number_special_char_form):  
    with app.test_request_context(): 
        form = LoginForm()
        field = does_not_contain_plaintext_password_contains_capital_number_special_char_form 
        with pytest.raises(ValidationError, match=r"Please include a number in the password field") as validation_error:  
            make_password_contain_number(form, field)
