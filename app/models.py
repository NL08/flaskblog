# from flaskblog folder in __init__.py
from datetime import datetime
from flask import flash, redirect, url_for
from flask_login import UserMixin
# itsdangergous... gives a time sensitive message 
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import db
from argon2 import PasswordHasher

class User(UserMixin, db.Model):
    '''
    one to many relationship between both tables.
    The One relationship.
    '''
    id = db.Column(db.Integer, primary_key=True)
    # unique blocks the same username
    # I can't have Nullable=False because it will make me add the columns everytime I add a column in User table
    username = db.Column(db.String(80), unique=True)
    hashed_password = db.Column(db.String(128))
    email = db.Column(db.String(120), unique=True)
    registration_confirmation_email = db.Column(db.Boolean, default=False)     
    profile_pic_name = db.Column(db.String())
    # relationship connects the tables.
    # db.relationship first argument is named after the many table. This creates a relationship between the 2 tables.
    # What does lazy do?
    # The value of backref allows to get a value from the other table?
    rel_posts = db.relationship('Posts', backref='profileinfo', lazy=True)
    rel_payments = db.relationship('Payments', backref='profileinfo', lazy=True)       
 
    def compare_hashed_passwords(self, hashed_password_db, plaintext_password_form):
        '''   
        The code runs in the /login route.
        Query the db for the hashed_password. 
        If not the value will be a different hash and the function ph.verify will return False even 
        if password_form is the same as in the register route.
        '''
        ph = PasswordHasher()
        try:
            self.verified_hashed_password = ph.verify(hashed_password_db, plaintext_password_form)
            return self.verified_hashed_password
        except:
            flash('The password does not exist in the db.')
            return redirect(url_for('auth.home')) # line have to redirect can it be a validation error? 



    def create_token(self, expires_sec=1800):
        SECRET_KEY = 'temp_secret_key'
        # Serializer passes in the SECRET_KEY for 30 min beacuse of expir_sec.
        s = Serializer (SECRET_KEY, expires_sec) 
        # This Creates the randomly assigned token for 30 min   
        return s.dumps({'users_id': self.id}).decode('utf-8')
            
    # use @staticmethod so I don't have to use the self variable. 
    @staticmethod
    def verify_token(token): # token is equal to create_token after called.  
        SECRET_KEY = 'temp_secret_key'
        # Serializer passes in SECRET_KEY
        s = Serializer(SECRET_KEY)

        try:
            # s.loads(token) gets the User's id by running
            users_id = s.loads(token)['users_id']   
        except:
            flash('This is an invalid or expired token') 
            # Why query.get? Because  "u = User.query.get(1)" gives the current user.
            return None
        return User.query.get(users_id)    
    
    # what does this do?
    def __repr__(self):
        return f"User('{self.email}')" 




class Posts(UserMixin, db.Model):
    '''
    one to many relationship between both databases.
    This is the Many relationship.
    '''

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.String(120), nullable=False) 
    # Everyone sees the same time based on daylight savings.  
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    '''
    When using the foreign key colmun use the name of the column of the other table except an lowercase and end it with _id.
    # The foreign key creates  an column called user.id. This links the two tables. 
    IOW the foreign key is the primary key just in another table.
    # user.id represents the id from the User database. 
    '''

    # If I have the Posts table and want a value from the user table to Posts.user.id.username?
    fk_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

    # what does this do?
    def __repr__(self):
        return f"Posts('{self.title}')" 




# if a user has an account the user will connect to the db if not it is not required.
class Payments(db.Model):
    '''
    One to many relationship
    This is the Many relationship. 
    '''
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(80))
    price_of_donation = db.Column(db.Integer)
    # How do I turn email into the foreign key? todo.
    email = db.Column(db.String(120))
    fk_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    def __repr__(self):
        return f"Payments('{self.email}')" 
    

    '''
    Uselist=False creates a one to one relationship instead of a 1 to many when using a foreign key etc
    relationship creates a connection between the foreign key table and the primary key table 
    is it okay as the same name as the table?
    Here is an example.
    '''