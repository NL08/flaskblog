import os

import bcrypt
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user
# from flask_mail import Message 
# itsdangergous... gives a time sensitive message 
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from redmail import gmail

from app import db, email, mail
from app.mail.forms import (EmptyForm, RequestResetPasswordForm,
                            ResetPasswordForm)
from app.models import User

# make bcrypt and db work 







# make the email variable below work. 
 

mail = Blueprint('mail', __name__, template_folder='templates')











#from redmail import EmailSender
# email = EmailSender(host="smtp.mail.com", port=587)
# why user.create_token(), because it is an method? 


# send account verification email for registration
# This function is in the /register route
def send_account_registration_email(user_db):
    # should I use a form?
    form = EmptyForm()
    # the function creates the randomly generated token
    token = user_db.create_token() # don't need to import methods just the class. # why don't I use arguments in create_token?
    # needed for gmail.send for gmail
    gmail.send(
            subject="register account",
            sender=os.environ['EMAIL_USERNAME'], 
            receivers=[user_db.email],
            # remember url for won't work for some reason.
            html = render_template('reset_email/verify_email.html', title='verify email', token=token, form=form, _external=True) 
    )
 




  


# This route is always a get request!!!
# verify the users email or after you clicked on the email from the recieved email
# better name for function maybe change to verify?
@mail.route("/verified_email<token>", methods = ['GET']) 
def verified_email(token):      
    user_db = User.verify_token(token)
    if user_db is None: # why does this not work pytest later??
        flash('This is an invalid or expired token')
        return redirect(url_for('auth.home'))   
    

    # Prevents you from registering twice. Is this needed?
    if user_db.registration_confirmation_email == True:
        flash('You have already clicked on the confirmation email. You can now login')
        return redirect(url_for('auth.home'))

    user_db.registration_confirmation_email = True 
    db.session.commit()
    
    form = EmptyForm()
    return render_template('verified_email.html', title='verified email', form=form)







def send_reset_password_email(user_db):
    # get the function from models.py
    token = user_db.create_token()
    # _external – if set to True, an absolute URL is generated. Server address can be changed via 
    # Absolute import is  https://example.com/my-page relative URL is  /my-page 
    form = EmptyForm()
    gmail.send(        
        subject='Password Reset Request', 
        sender=os.environ['EMAIL_USERNAME'],  # change to noreply...?
        receivers=[user_db.email],   
        html = render_template('send_reset_password_email.html', title='send reset password email', token=token, form=form, _external=True)
    )
    
# creates form for email when you reset password 
# better name
@mail.route("/request_reset_password", methods = ['POST', 'GET'])
def request_reset_password():
    form = RequestResetPasswordForm()
    if form.validate_on_submit():   
        
        email_form = form.email.data
        user_db = User.query.filter_by(email=email_form).first()
      
        # if the user is not registered and you have not clicked  
        if not user_db:
            flash('Your email is not registered. Please register first.')
            return redirect(url_for('mail.request_reset_password')) 
        
        # make sure the user clicks on the registration email before resetting the password
        if user_db.registration_confirmation_email  == False: 
            flash('You have not clicked on the email to register yet. Please click on it before you can reset your password.')
            return redirect(url_for('mail.request_reset_password'))  
       
        

        flash("An email has been sent with instructions to your email to reset the password") 
        send_reset_password_email(user_db)
        return redirect(url_for('auth.home'))
    return render_template('request_reset_password.html', title='request reset password', form=form)




# reset password after recieved the token in a email
# create form for password field and confirm password
@mail.route("/reset_password/<token>", methods = ['GET', 'POST'] )
def reset_password(token):
 
    form = ResetPasswordForm()
    if form.validate_on_submit():   
        user_db = User.verify_token(token)
        if user_db is None: # make sure user exists, do I need this probably not because of the code below.
            flash('This is an invalid or expired token', 'warning')
            return redirect(url_for('mail.request_reset_password'))    
        # make sure the user clicks on the registration email before resetting the password
        if user_db.registration_confirmation_email  == False: 
            flash('You have not clicked on the email to register yet. Please click on it before you can reset your password.')
            return redirect(url_for('mail.request_reset_password'))  
     
        plaintext_password_form = form.password.data
        confirm_password_form = form.confirm_password.data
        
        if plaintext_password_form != confirm_password_form:
            flash("The passwords fields do not match" ) # I need better phrases. 
            return redirect(url_for('mail.request_reset_password'))   
        
        # example password
        plaintext_password = form.password.data
        # converting password to array of bytes
        bytes = plaintext_password.encode('utf-8')
        # generating the salt
        salt = bcrypt.gensalt()
        # Hashing the password
        hashed_password = bcrypt.hashpw(bytes, salt)        
        

        user = User(hashed_password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('you have changed your password successfully')
        return redirect(url_for('auth.home')) 


    # why does render_template need to go not in the POST if statement?? Confirm
    return render_template('reset_password.html', title='reset password', token=token, form=form) 

















