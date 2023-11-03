import os
from flask import flash
env = os.environ.get('TEST_ENV', 'DEV_ENV')
from app import app

# allow different imports so the code works during pytest + None pytest
if app.config['ENV'] == 'development':
    from app.models import User, Payments
elif app.config['ENV'] == 'pytest': 
    from app.tests.models import UserTest as User ,PaymentsTest as Payments

from app import db
# fix this function the env part
def add_foreign_key(email_form):
    '''
    This runs in the /donation route.
    if the email exists in the User table and the email exists in the Payment table exists add the FK.
    The function only works if you are making a donation with an User who has an account.
    You will always have a registered account when adding Foreign key. 
    '''
    user_db = User.query.filter_by(email=email_form).first()
    payment_db = User.query.filter_by(email=email_form).first()
    # makes sure the tables are not None / empty list + contain same emails in the db 
    if User.query.filter_by(email=email_form).first() and User.query.filter_by(email=email_form).first() and user_db.email == payment_db.email: 
        # In the db I have a FK for Payments column called fk_user_id and the PaymentsTests column called fk_usertest_id.
        # Because the pytest db and non pytest db have have different names I need the conditionals
        if app.config['ENV'] == 'development':
            user_id_db = user_db.id
            payments = Payments(fk_user_id=user_id_db)
            db.session.add(payments)
            db.session.commit()
        else: # for pytest
            user_id_db = user_db.id
            payments = Payments(fk_usertest_id=user_id_db)
            db.session.add(payments)
            db.session.commit()
        flash('Success the Foreign key is added')
        return 'success'
    else:
        print('The Foreign key is not added')    
        return None





 