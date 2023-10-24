# from flaskblog folder in __init__.py
from datetime import date, datetime

from flask import flash, redirect, url_for
from flask_login import LoginManager, UserMixin
# itsdangergous... gives a time sensitive message 
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import Column, Integer, LargeBinary, String

from app import db

# https://stackoverflow.com/questions/63231163/what-is-the-usermixin-in-flask


'''
many to many relationship.
I have 2 foreign keys from the User table.  
'''
Followers = db.Table('followers',

    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')) )

from argon2 import PasswordHasher

class User(UserMixin, db.Model):
    '''
    one to many relationship between both tables.
    The One relationship.
    '''
    id = db.Column(db.Integer, primary_key=True)
    # unique blocks the same usernames
    # I can't have Nullable=False because it will make me add the columns everytime I add a column in User table
    username = db.Column(db.String(80), unique=True)
    hashed_password = db.Column(db.String(128))
    email = db.Column(db.String(120), unique=True)
    registration_confirmation_email = db.Column(db.Boolean, default=False)     
    profile_pic_name = db.Column(db.String())
    # relationship connects the tables.
      
 

    
    def compare_hashed_passwords(self, hashed_password_db, plaintext_password_form):
        '''   
        The code runs in the /login route.
        You should query the db for hashed_password 
        or the value will be a different hash; 
        and the function ph.verify will return False even 
        if the password form match with the hash password.
        '''
        
        ph = PasswordHasher()
        try:
            self.verified_hashed_password = ph.verify(hashed_password_db, plaintext_password_form)
            return self.verified_hashed_password
        except:
            flash('The password does not exist in the db.')
            return redirect(url_for('auth.home'))
        # have to redirect 
    

    '''
  
    The name of the db.relationship column is named after the many table. Ex Posts
    relationship creates the connection between the 2 databases.
        lazy?
    '''
    
    '''
    Take the value of backref to get a column from the current table from the other databases. 
    The current table is User and backref is either = payment or post.
    ex 
    post.username or post.payments 
    '''
    
    rel_posts = db.relationship('Posts', backref='profileinfo', lazy=True)
    rel_payments = db.relationship('Payments', backref='profileinfo', lazy=True) 

    '''
    Create Many to many relationship
    '''
    
    # relationship creates the connection by the database? 
    followed = db.relationship(
        # 'User' is the right table and left table
        # secondary - configures the association followers table? 
        # child table has 2 foreign keys in one table.
        'User', secondary=Followers,
        # primaryjoin links the followers_id with the the user_id.
        primaryjoin=(Followers.c.follower_id == id),
        # secondaryjoin links the followed_id with the user_id.
        secondaryjoin=(Followers.c.followed_id == id),
        # backref - defines how the right and left side entity will be accessed. 
        # get the right and left side entity from the followers table 
        # lazy?
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
  
        
    # why functions like this and here?
    def follow(self, user):
        #  .is_following(user) is False. IOW I am not following an user
        if not self.is_following(user):
            self.followed.append(user)
            return self
        
    def unfollow(self, user):
        # .is_following(user) is True. IOW I am following an user
        if self.is_following(user):
            self.followed.remove(user)
            return self
        # check if it is_following
    def is_following(self, user):
        # followers_id = user_id if it is already following an user_id. 
        # Instead of followers.c.followed_id == user.id I am saying user.id == user.id.
        # 1 > 0 returns True and  0 > 0 returns False. 
        return self.followed.filter(Followers.c.followed_id == user.id).count() > 0
    
    
    
    
    
    
    
    
    
    # show blog posts written by all the people that are followed by the logged in user. 
    # The query scales well and allows pagination and the correct date vs going user.followed.all().          
    def followed_posts(self):
        # The join condition creates a temporary table that combines data from the Posts table and the followers table. It gives me all the Posts I am following/followed! 
        # followers.c.followed_id == Posts.user_id. If it is not True then you are not following an user and you want to be following an user. 
        # I can create a table that has more then one user who follows using followers.c.followed_id == Posts.user_id.      
        followed = Posts.query.join(
            # filter followers.c.follower_id == self.id selects me all the posts of one user! self.id?
            Followers, (Followers.c.followed_id == Posts.User_id)).filter(
                Followers.c.follower_id == self.id)
        # The query above works except it does not include the users own posts in the timeline. Use the line below to do that. 
        own = Posts.query.filter_by(User_id=self.id)
        # combines the followed query with the own query using union
        # Posts.timestamp.desc lists the posts in order in desc order of when they were posted.
        return followed.union(own).order_by(Posts.timestamp.desc())



    # How does this get the current_id? By using self. 
    def create_token(self, expires_sec=1800):
        SECRET_KEY = 'temp_secret_key'
        # Serializer passes in the SECRET_KEY for 30 min beacuse of expir_sec.
        s = Serializer (SECRET_KEY, expires_sec) 
        # This Creates the randomly assigned token for 30 min   
        return s.dumps({'users_id': self.id}).decode('utf-8')
            


            
    # Why use @staticmethod? So I don't have to use the self variable. 
    @staticmethod
    def verify_token(token): # token is equal to create_token.  
        # Serializer passes in SECRET_KEY
        SECRET_KEY = 'temp_secret_key'
        s = Serializer(SECRET_KEY)

        try:
            ''' 
            Gets the user id by running s.loads(token), if this line works.  
            If it does not work returns error and return none in the except block
            '''
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

    # If I have the Posts table and want a value from the user table to Posts.user.id.username
    fk_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

    # what does this do?
    def __repr__(self):
        return f"Posts('{self.title}')" 




 # should I connect this to User's table? Yes 
 
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