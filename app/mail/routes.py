import os

from flask import Blueprint, flash, redirect, render_template, url_for
# itsdangergous... gives a time sensitive message 
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from redmail import gmail

from app import db, mail
from app.mail.forms import (EmptyForm, RequestResetPasswordForm,
                            ResetPasswordForm)
from app.models import User

mail = Blueprint('mail', __name__, template_folder='templates')



# send email to your email account. 
# This function is in the /register route
def send_account_registration_email(user_db): # should I move this and rename it ? Probably
    
    form = EmptyForm()
    # creates a randomly generated token
    token = user_db.create_token()  
    # needed for gmail 
    gmail.send(
            subject="register account",
            sender=os.environ['EMAIL_USERNAME'], 
            receivers=[user_db.email],
            # remember url_for won't work in redmail , why?
            html = render_template('reset_email/verify_email.html', title='verify email', token=token, form=form, _external=True) 
    )
 




  


# This route is always a get request!!!
# This is after you clicked on the send_account_registration_email from your email account.
@mail.route("/verified_email<token>", methods = ['GET']) 
def verified_email(token):      
    user_db = User.verify_token(token)
    if user_db is None:  
        flash('This is an invalid or expired token')
        # Should I delete the user?
        db.session.delete(user_db)
        db.session.commit()
        flash("The user is deleted")
        return redirect(url_for('main.home'))   
    
    # Prevents you from registering twice.  
    if user_db.registration_confirmation_email == True:
        flash('You have already clicked on the confirmation email. You can now login')
        return redirect(url_for('main.home'))  
    
    user_db.registration_confirmation_email = True 
    true_boolean = user_db.registration_confirmation_email
    adding_true_boolean = User(registration_confirmation_email=true_boolean)
    db.session.add(adding_true_boolean)
    db.session.commit()
    
    form = EmptyForm()
    return render_template('verified_email.html', title='verified email', form=form)


# email sent in the code below
def send_reset_password_email(user_db):
    # get the function from models.py
    token = user_db.create_token()

    form = EmptyForm()
    gmail.send(        
        subject='Password Reset Request', 
        sender=os.environ['EMAIL_USERNAME'],  # change to noreply...?
        receivers=[user_db.email],   
        html = render_template('send_reset_password_email.html', title='send reset password email', token=token, form=form, _external=True)
    )
    
# creates password forms to reset your email
# After you filled out the password forms you are sent an email in your email account
@mail.route("/request_reset_password", methods = ['POST', 'GET'])
def request_reset_password():
    form = RequestResetPasswordForm()
    if form.validate_on_submit():   
        email_form = form.email.data
        user_db = db.session.execute(db.select(User).filter_by(email=email_form)).scalar_one_or_none()
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
        return redirect(url_for('main.home'))
    return render_template('request_reset_password.html', title='request reset password', form=form)

from argon2 import PasswordHasher


# This route is triggered after you clicked on the send_reset_password_email in your email account
# create form for password field and confirm password
@mail.route("/reset_password/<token>", methods = ['GET', 'POST'] )
def reset_password(token):
    form = ResetPasswordForm()   
    if form.validate_on_submit():

        plaintext_password_form = form.password.data
        confirm_password_form = form.confirm_password.data

        user_db = User.verify_token(token)
        if user_db is None: 
            flash('This is an invalid or expired token')
            return redirect(url_for('mail.request_reset_password'))    
        # make sure the user clicks on the registration email before resetting the password
        if user_db.registration_confirmation_email  == False: 
            flash('You have not clicked on the email to register yet. Please click on it before you can reset your password.')
            return redirect(url_for('mail.request_reset_password'))  
             
        if plaintext_password_form != confirm_password_form:
            flash("The passwords fields do not match" ) # I need better phrases. 
            return redirect(url_for('mail.request_reset_password'))   
                
        ph = PasswordHasher()
        hashed_password_form  = ph.hash(plaintext_password_form)
        user = User(hashed_password=hashed_password_form)
        db.session.add(user)
        db.session.commit()

        flash('you have changed your password successfully')
        return redirect(url_for('main.home')) 

    return render_template('reset_password.html', title='reset password', token=token, form=form) 

















