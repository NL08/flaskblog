import os
env = os.environ.get('TEST_ENV', 'DEV_ENV')
# allow different imports so the code works during pytest + None pytest
current_config = os.environ['FLASK_ENV']
if current_config == 'dev':
    from app.models import Payments, User
elif current_config == 'test':
    from app.tests.models import UserTest as User, PaymentsTest as Payments


from flask import flash
from app import db

# fix this function the env part
def add_foreign_key(email_form):
    '''
    This runs in the /donation route.
    if the email exists in the User table and the email exists in the Payment table exists add the FK.
    The function only works if you are making a donation with an User who has an account.
    You will always have a registered account when adding Foreign key. 
    '''
    user_db = db.session.execute(db.select(User).filter_by(email=email_form)).scalar_one_or_none()
    payment_db = db.session.execute(db.select(Payments).filter_by(email=email_form)).scalar_one_or_none()
    # makes sure the tables are not (None / empty) list + contain same emails in the db 
    if user_db and payment_db:
        if user_db.email == payment_db.email: 
            user_id_db = user_db.id
            payments = Payments(fk_user_id=user_id_db)
            db.session.add(payments)
            db.session.commit()
            flash('Success the Foreign key is added')
            return 'success'
    # executes if the "if" statements don't activate?    
    print('The Foreign key is not added')    
    return None





 