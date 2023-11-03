import stripe
from flask import Blueprint, flash, redirect, render_template, request, url_for
from app.payment.forms import EmailForm, EmptyForm  
payment = Blueprint('payment', __name__, template_folder='templates')
# import db from flaskblog folder in __init__.py.
from app import db
from app.models import Payments
'''
# This is before the table was created.
products = {
    'donations': 
    {
        'name': 'Donation for the site',
        'price': 500, # 500 is = 5.00 , how do I use a counter? Answer turn into a table in a database
    }
}
'''
from app.payment.functions import add_foreign_key
@payment.route('/donations', methods = ['POST', 'GET'])
def donations():
    
    form = EmailForm()
    if form.validate_on_submit():
        ''' 
        Start off as a decimal float then you mulitply by 100 to get the cents. An ex int ex .55 then get 55.0,
        then convert from float to int then to string because request.form uses str/strings.
        '''
        # The reason you do the converting from a decimal float to a int because sql can't store decimals. 
        price_of_donation_form = str(int(float(request.form["number"]) *100) ) # Make global variable? 
        if not price_of_donation_form: # emp
            flash('You did not type in a donation price.')
            # 307 redirects to the route while being a POST request
            return redirect( url_for('payment.donations.html'), code=307 )
        email_form = form.email.data
        payment_db = Payments(price_of_donation=price_of_donation_form, item_name='Donate' , email=email_form) 
        db.session.add(payment_db) 
        db.session.commit()
    
        add_foreign_key(email_form)        
        # 307 allows the redirects to redirect to a POST request
        return redirect(url_for('payment.order', item_name_db=payment_db.item_name), code=307)
                
    return render_template('stripe_payment/donations.html',  form=form, title=' Give donations')


@payment.route('/order/<item_name_db>', methods=['POST'])
def order(item_name_db):

    payment_db = Payments.query.filter_by(item_name=item_name_db).first_or_404()
    '''
    you can only purchase one product at a time, but since line_items is a list, 
    you can select and buy multiple products if you add a shopping cart interface
    ''' 
    checkout_session = stripe.checkout.Session.create(   
        # The line_items argument specifies the product that the user wishes to buy.
        line_items=[
            {
                'price_data': {
                    'product_data': {
                        'name': payment_db.item_name, 
                    },
                 
                    # automatically converts to decimals/float
                    'unit_amount': payment_db.price_of_donation,
                    'currency': 'usd',
                },
                'quantity': 1,
            },
        ],         
        # prefill the email input in the form.
        # I use this so I don't have 2 different emails in 2 different forms.  
        customer_email=payment_db.email,
        # payment_method_types argument allows what payment you want/allow.
        payment_method_types=['card'],
        # mode specifies what type of payment you want. An example is payment is a one time payment. 
        mode='payment',
        # stripe will redirect to one of these pages upon the form completion. How?
        success_url=request.host_url + 'order/success',
        cancel_url=request.host_url + 'order/cancel',
    )
    return redirect(checkout_session.url)
 



@payment.route('/order/success')
def success():
    return render_template('success.html')


@payment.route('/order/cancel')
def cancel():
    # send email 
    return render_template('cancel.html')

 




