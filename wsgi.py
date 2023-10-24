import os

from flask_migrate import Migrate
from app import create_app, get_multiple_configs 

app = create_app(get_multiple_configs())

from app import db


db.init_app(app)

migrate = Migrate(app, db)

from app.auth.forms import SearchForm 
 
 
@app.context_processor
def layout():
    '''
    # Pass Stuff to Navbar such as form in layout.html
    
    If I don't pass on the form in base function then I will 
    get an error in layout.html because of {{form.csrf_token}} 
    ''' 
    form = SearchForm()
    return dict(form=form)     






# to run the code
'''
To setup the app to run from a specific file type the line below. Only do Once.
$env:FLASK_APP="wsgi"
To use the debugger use this line.
$env:FLASK_ENV="development"
flask run
'''

 

 