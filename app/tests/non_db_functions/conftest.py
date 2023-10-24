'''To print print statements and to print pytest type in terminal use 
'pytest -q --capture=no ' '''



import os

import bcrypt
import pytest


from wsgi import app

@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture
def runner():
    return app.test_cli_runner()



@pytest.fixture
def username_form():
    
    username = 'fkpr[kfkuh'
    return username

# MODIFLY 
@pytest.fixture
def hashed_password_form():    
   
    plaintext_password = 'pojkp[kjpj[pj'
    # converting password to array of bytes
    bytes = plaintext_password.encode('utf-8')
    # generating the salt
    salt = bcrypt.gensalt()
    # Hashing the password
    hashed_password_form = bcrypt.hashpw(bytes, salt)
    return hashed_password_form



@pytest.fixture 
def email_form(): 

    #email_form = os.environ['TESTING_EMAIL_USERNAME']
    email_form = 'nmyles@mail.com'
    return email_form 




#def plaintext_password_form():






from app import db
from app.tests.models import UserTest
from wsgi import app


@pytest.fixture
def yield_nonexistent_form():  
    
    '''
    This is in the /register route
    The form can be for the username or email
    Create the db column then yield the nonexistent_form_in_db = 'zbkjuhnbuh' and finally delete the db.
    yield does not stop the code when yielded.
    '''

   
    with app.test_request_context(): # = with app.app_context() except won't work for pytest
        bind_key="testing_app_db"
    
        def _subfunction(username_form, hashed_password_form, email_form):
            # Create the database and the database table
            db.create_all(bind_key)
            usertest_db = UserTest(username=username_form, hashed_password=hashed_password_form, email=email_form)
            db.session.add(usertest_db)
            db.session.commit()
            nonexistent_username = 'zbkjuhnbuh'
            return nonexistent_username
        # yield unlike return doesn't stop when called.
        yield _subfunction 
        db.drop_all(bind_key) 
 






@pytest.fixture
def yield_usertest_db():  
    '''

    This is in the /register  route
    Create the db column then yield the selected/queried usertest and finally delete the db.
    yield does not stop the code when yielded.
    '''

    # = with app.app_context() except won't work for pytest
    with app.test_request_context():

        bind_key="testing_app_db"

        def _subfunction(username_form, hashed_password_form, email_form):
            # Create the database and the database table
            db.create_all(bind_key)
            usertest_db = UserTest(username=username_form, hashed_password=hashed_password_form, email=email_form)
            db.session.add(usertest_db)
            db.session.commit()
            # Why can't current_usertest_db be the same name as usertest_db here?
            current_usertest_db = UserTest.query.filter_by(username=username_form).first()   
            return current_usertest_db 
            #return username_form 

         # yield unlike return doesn't stop when called.
        yield _subfunction 
        db.drop_all(bind_key) 

