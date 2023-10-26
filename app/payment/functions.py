

import os

from flask import flash

env = os.environ.get('TEST_ENV', 'DEV_ENV')

from app import app
# allow different imports so the code works during pytest + None pytest
if app.config['ENV'] == 'development':
    from app.models import User, Payments
elif app.config['ENV'] == 'pytest': 
    from app.tests.models import UserTest as User , PaymentsTest as Payments
      

from app import db

# fix this function the env part
def add_foreign_key(email_form):
    
    '''
    This runs in the /donation route.
    if the email exists in the User table and the email exists in the Payment table exists add the FK.
    You will always have a registered account when adding Foreign key. 
    '''
    
    user_db = User.query.filter_by(email=email_form).first()
    payment_db = User.query.filter_by(email=email_form).first()
    # makes sure the tables are not None / empty list + contain same emails in the db 
    if User.query.filter_by(email=email_form).first() and User.query.filter_by(email=email_form).first() and user_db.email == payment_db.email: 

    # In payment_db and user_db
        # user.id is the foreign key in the Payment database. You need to manually add FK's.   
        user_id_db = user_db.id
        print(user_id_db)
        # This is used because I have 2 different FK names in models.py 1 for pytest + not pytest 
        if env == 'test':
            paymentstest = Payments(fk_usertest_id=user_id_db)
            db.session.add(paymentstest)
            db.session.commit()
        else:
            payments = Payments(fk_user_id=user_id_db)
            db.session.add(payments)
            db.session.commit()
        flash('Success the Foreign key is added')
    else:
        print('The Foreign key is not added')    
        return None





 