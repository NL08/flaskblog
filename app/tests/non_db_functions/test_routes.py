from app.auth.functions import make_password_contain_capital, make_password_contain_number
from wsgi import app

from app.auth.forms import LoginForm
from wtforms.validators import ValidationError
import pytest

from collections import namedtuple




@pytest.fixture
def plaintext_password_contains_capital_number_special_char_form():
    field = namedtuple('field', ['data'])
    password_form = field('Aejfpwo;fkj4eo;')
    return password_form






def test_password_with_capital(plaintext_password_contains_capital_form):
   
    with app.test_request_context(): 
        form = LoginForm()
        field = plaintext_password_contains_capital_form
        contains_capital = make_password_contain_capital(form, field) 
        
        with pytest.raises(ValidationError):  
            contains_capital    


 

def test_password_with_capital(plaintext_password_contains_capital_number_special_char_form):
   
    with app.test_request_context(): 
        form = LoginForm()
        field = plaintext_password_contains_capital_number_special_char_form
        contains_capital = make_password_contain_capital(form, field) 
        
        with pytest.raises(ValidationError):  
            contains_capital    




def test_password_with_number(plaintext_password_contains_capital_number_special_char_form):
   
    with app.test_request_context(): 
        form = LoginForm()
        field = plaintext_password_contains_capital_number_special_char_form
        contains_capital = make_password_contain_number(form, field) 
        
        with pytest.raises(ValidationError):  
            contains_capital    




def test_register_page_post(client):
    with app.test_request_context():    
        response = client.post('/register', data = {'username':'zzz', 'password':'rrrrrrrrrrrrrrr' })
        assert b"This text doesn't exist" in response.data
        assert response.status_code == 300
    
    #with client:  
    '''
    GIVEN a Flask application configured for testing
    WHEN the '/register requested (GET) 
    THEN check that the response is valid 
    '''
    
    #response = client.get('/register', follow_redirects=True)
    '''
    In Python, the assert statement will execute if the given condition evaluates to True. 
    If the assert condition evaluates to False, then it raises an assertion Error exception with the specified error message.
    '''
    ## Why use a b string? What is response.data? Answer it only work  I have a status code 200.
    #assert response.status_code == 200
    # checks the html for the string register
    #assert b'register' in response.data
    #with app.test_request_context():
     








 



'''
app = create_app(PostPytestConfig) is needed instead of app = create_app(PytestConfig). If I want to use
the try in a Post request in pytest, pytest blocks Post requests becasue it requires form.crsf_token.
I also I need to create a new client and runner fixtures to get it to work with Post.
'''


 

def test_register_page_post(client): 
    ''' 
    GIVEN a Flask application configured for testing
    WHEN the '/register requested (POST) 
    THEN check that the response is valid 
    '''  
    response = client.post('/register', follow_redirects=True)
    assert response.status_code == 200
    assert b'register' in response.data
     
#from app.auth.forms import LoginForm
 
#def test_register_page_post(client, yield_usertest_db): 
    ''' 
    GIVEN a Flask application configured for testing
    WHEN the '/register requested (POST) 
    THEN check that the response is valid 
    '''  
    
#    response = client.post('/register', follow_redirects=True , data = {'username': yield_usertest_db})
#    assert response.status_code == 200
#    assert b'register' in response.data
#    with app.test_request_context():

#        form = LoginForm()

#        username_form = form.username.data  
#        assert username_form == 'ggggggggg'






def test_verified_email_post_get(client):   
    ''' 
    GIVEN a Flask application configured for testing
    WHEN the "/verified_email<token>" request is (GET) Also test the token is created and verified. email is sent
    THEN check that a token works.
    '''   
    

    response = client.get("/verified_email<token>", follow_redirects=True) # what is this?
    assert response.status_code == 200
    # with app.test_request_context():                    





