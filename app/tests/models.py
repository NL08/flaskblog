# itsdangergous... gives a time sensitive message 
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import db


class UserTest(UserMixin, db.Model):
    __tablename__ = 'user_test'
    __bind_key__ = "testing_app_db"
    id = db.Column(db.Integer, primary_key=True)
    # unique blocks the same usernames
    # I can't have Nullable=False because it will make me add the columns everytime I add a column in User table
    username = db.Column(db.String(80), unique=True)
    hashed_password = db.Column(db.String(128))
    email = db.Column(db.String(120), unique=True)
    registration_confirmation_email = db.Column(db.Boolean, default=False) 
    # need a better backref name.
    rel_payments = db.relationship('PaymentsTest', backref='profileinfo', lazy=True)
    bind_key = "testing_app_db"

    def create_token(self, expires_sec=1800):
        SECRET_KEY = 'temp_secret_key'
        # Serializer passes in the SECRET_KEY for 30 min beacuse of expir_sec.
        s = Serializer (SECRET_KEY, expires_sec) 
        # This Creates the randomly assigned token for 30 min. This is a string.
        return s.dumps({'Users_id': self.id}).decode('utf-8')
    
    def __repr__(self):
        return f"<UserTest('{self.email}')>" 
 


            
class PaymentsTest(db.Model):
    '''
    One to many relationship
    This is the Many relationship. 
    '''
    __bind_key__ = "testing_app_db"
    __tablename__ = 'payments_test'
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(80)) # what value should this be
    price_of_donation = db.Column(db.Integer)
    # How do I turn email into the foreign key? todo.
    email = db.Column(db.String(120))     
    fk_user_id = db.Column(db.Integer, db.ForeignKey('user_test.id'))
    bind_key = "testing_app_db"
    # what does this do?
    def __repr__(self):
        return f"<PaymentsTest('{self.email}')>" 
 