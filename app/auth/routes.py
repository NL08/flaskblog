# Continue 25:31 https://www.youtube.com/watch?v=803Ei2Sq-Zs
import os
# random generator
import uuid

from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

# from werkzeug.datastructures import FileStorage

'''
# Is there another way to do this.
# import create_app or app app.elasticsearch... 
from app import create_app
# import Config to get create_app to work 
from app.config import Config
app = create_app(Config)
'''
from flask import Blueprint, flash, redirect, render_template, request, url_for

# make @auth work from userinfo folder in this file 
auth = Blueprint('auth', __name__, template_folder='templates')

''' 
# todo turn into a database why is there no post number like 1st post ever posted in general etc?
posts = {   
    "username": "author",
    "author": "Bobby Bobson",
    "Title": "Hello World",
    "Content": "This is a post content 1",
    "date_posted": "March 17 2021" 
}
'''


''' IMPORTANT flash not working before a redirect why? '''
 
 




@auth.route("/")
@auth.route("/home")
def home():  
    
   

    posts = Posts.query.all()
    # add_to_index('F', posts)
    return render_template('home.html', posts=posts, title='home')  

# import db from flaskblog folder in __init__.py
from app import db, app 
from app.auth.forms import FileForm
from app.models import Posts, User



@auth.route('/profile/<string:username>', methods = ['GET'])
def profile(username): 

    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', title='profile',user=user)
    



# todo change don't need here?
# basedir_for_uploads = os.path.abspath(os.path.profilepictures(__file__)
app.config['UPLOAD_FOLDER'] = r"C:\Users\nmyle\OneDrive\Desktop\flaskcodeusethis\flaskblog2\app\static\profilepictures"
# remember todo add max file size for uploads
# I might want to use this route below and the .html name?
# @auth.route('/upload/profile/<string:username>', methods = ['GET'])
@auth.route('/upload_picture', methods=['GET', 'POST'])
def upload_picture():
    
    # if the user is not logged in make it so they can't go to the login page. 
    if not current_user.is_authenticated:
        return redirect(url_for('auth.home')) 
    
    form = FileForm()
    if form.validate_on_submit():
        picture_filename = form.image_filename.data     
         # Make file secure...         
        # This makes sure the filename is safe
        filename_is_secure = secure_filename(picture_filename.filename)
        
        # make the file unique incase someone uploads the same name
        # uuid is a random number generator
        unique_filename = str(uuid.uuid1()) + filename_is_secure
        upload = User(profile_pic_name=unique_filename)
        db.session.add(upload)
        db.session.commit()
        # save file to a secure location
        picture_filename.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))   
        flash("You have succesfully uploaded your profile picture.")
        return redirect(url_for('auth.profile', username=current_user.username)) # double check this

    return render_template('upload_picture.html', form=form, title='upload Profile Picture') 

from app.auth.forms import EmptyForm

'''move to different route.py keep with profile.'''
@auth.route("/followers/<string:username>", methods = ['Get', 'Post'])
# can if user is None be replaced by @login_required
@login_required
def followers(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first_or_404() 	
        # methods from models.py don't need self
        is_following = is_following(user)
        if (is_following == False):
            current_user.follow(user)
            db.session.commit()	
            return render_template( 'followers.html', title='follow', form=form, is_following=is_following, username=user.username)
        
        else:
            current_user.unfollow(user)
            db.session.commit()
            return render_template( 'followers.html', title='unfollow', form=form, is_following=is_following, username=user.username )

    return render_template( 'profile.html', title='followers', form=form, username=user.username)


 



@auth.route("/about")
def about():
    return render_template('about.html', title='register')







from app.auth.forms import RegistrationForm
from argon2 import PasswordHasher
from app.mail.routes import send_account_registration_email  

@auth.route("/register", methods = ['POST', 'GET'])
def register():

    # if the user is logged in make so they can't go to the register page. 
    if current_user.is_authenticated:
        return redirect(url_for(('auth.home')))
    
    form = RegistrationForm()
    # form.validate_on_submit(): are always the same line of render template to always allow a get request.
    if form.validate_on_submit():

        username_form = form.username.data
        email_form = form.email.data
        plaintext_password_form = form.password.data
        confirm_plaintext_password_form = form.confirm_password.data
        # hash the password I assume you can't turn this into a function  
        ph = PasswordHasher()
        hashed_password_form  = ph.hash(plaintext_password_form)
        
        adding_user = User(username=username_form, email=email_form, hashed_password=hashed_password_form)
        db.session.add(adding_user)
        db.session.commit()
                
        user_db = User.query.filter_by(username=username_form).first()
        send_account_registration_email(user_db) 
        flash('You have almost registered successsfully. Please click the link in your email to complete the registeration.')                
            
        return redirect(url_for('auth.login'))
    return render_template('register.html',title='register', form=form)



from app.auth.forms import LoginForm

@auth.route("/login",methods = ['POST', 'GET'])
def login():
    # if the user is logged in make it so they can't go to the login page. 
    if current_user.is_authenticated:
        return redirect(url_for('auth.home')) 

    form = LoginForm()
    if form.validate_on_submit():
        username_or_email_form = form.username_or_email.data
        username_db = User.query.filter_by(username=username_or_email_form).first()                
        email_db = User.query.filter_by(email=username_or_email_form).first() 

        if username_db:
            if username_db.username == username_or_email_form:
                user_db = username_db
        

        elif email_db:
            if email_db.email == username_or_email_form:
                user_db = email_db
        
           
        else:
            flash('username or email do not exist')
            return redirect(url_for('auth.login')) 
                

        plaintext_password_form = form.password.data
            
        registration_confirmation_email = user_db.registration_confirmation_email
        if registration_confirmation_email == False:
            flash('You have almost registered successfully. Please click the link in your email to complete the registeration.')
            return redirect(url_for('auth.login'))
        # checks if an hashed_password is not an empty field + matches hashed password in db. 
        hashed_password_db = user_db.hashed_password
            #todo delete
            #plaintext_password_form2 = 'wrong_string'
            #plaintext_password_form2 = plaintext_password_form.encode('utf-8')
            #if str(plaintext_password_form) == 'dsssssssssssssssssss':
            #    flash(plaintext_password_form)
            #    flash('the password is not a string')
            #    return redirect(url_for('auth.login'))
        
            # hash the password    
            
                
        user_db.compare_hashed_passwords(hashed_password_db, plaintext_password_form)
    
      




            # login_user(user, remember=form.remember.data)
        login_user(user_db)
        flash('You have logged in successfully') 
        '''           
                    
            To determine if the URL is relative or absolute, check it with Werkzeug's url_parse() function and then check 
            if the netloc component is set or not. What is netloc?
                    
                next = '/login?next=/index', index is just a route. 
                The 'next' variable can have 3 values

                1st value)
                If the login URL does not have a next argument you will be logged in and redirected to the home page.
                iow's next = '/login?next=/' '.  
                    
                How would the other 2 situations happen?

                2nd value)
                if the user is not logged in and tries to go to a route with @login_required, then for example post/new_post ,
                iow's 'next = login?next=/post/new_post' . (This is relative import).
                
                3rd value)
                To protect from redirect to any other website, in the module it checks if next is relative or full url. 
                if it's full domain then, the user is redirected to home page. 
                '''
        # does this check the current route?
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('auth.home')
        return redirect(next_page)

    return render_template('login.html', title='login', form=form)






 

 

from app.auth.forms import SearchForm






 
@auth.route('/search', methods= ['GET', 'POST'])
def search():  
    form = SearchForm()


    
    if form.validate_on_submit():
 
        post_searched_form = form.searched.data
        #  "like" returns search results that are similar to the search form What does '%' do ?
        search_results = Posts.query.filter(Posts.content.like('%' + post_searched_form + '%')).order_by(Posts.title).all()
  

        return render_template('search.html', form=form, search_results=search_results)
    else:
        return redirect(url_for('auth.home'))

 
@auth.route("/logoff")
@login_required
def logoff():
    logout_user()
    return redirect(url_for('auth.home'))
                  


 