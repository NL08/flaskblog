# __init__.py in not in users folder  
from flask import Flask
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_redmail import RedMail
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

# Setup CSRF protection. This allows html forms to work and be secure
csrf = CSRFProtect()
# make mail work
email = RedMail()
ckeditor = CKEditor() 
app = Flask(__name__)
# Make @login_required work
login_manager = LoginManager(app)
# You get a custom login message when @login_required appears in the code.
login_manager.login_message_category = 'Login is required'
# Should I use auth.login ? What is this?
login_manager.login_view = 'login' 
# setup databases
db = SQLAlchemy()
#for flask migrate
migrate = Migrate(app, db)

from app.models import User
# Use User.query.get instead of User.get because of sqlalchemy ?
# This function logs you in and since there is no way of storing it in the database I need the function.
# Add @app because of the way the app is structured.
@app.login_manager.user_loader
def load_user(id):
    return User.query.get(id) 
 
from app.config import DevelopmentConfig, PytestConfig
def get_multiple_configs():    
    '''
    Allows multiple configs.
    For example if I type in the terminal development,
    I will get that config. 
    '''
 
    if app.config['ENV'] == 'development':
        env_name = DevelopmentConfig
        return env_name  
    elif app.config['ENV'] == 'pytest': 
        env_name = PytestConfig
        return env_name
         
def create_app(config_env=get_multiple_configs): 
    # The function name is from the config file which is "Class config:".
    app.config.from_object(config_env)
    migrate.init_app(app, db)
    db.init_app(app)
    login_manager.init_app(app)
    email.init_app(app)
    csrf.init_app(app) 
    # blocks this from pytest. Because I get a weird error when it runs in pytest
    if app.config['WTF_CSRF_ENABLED'] == True:
        ckeditor.init_app(app)
   
    from app.auth.routes import auth
    from app.mail.routes import mail
    from app.payment.routes import payment
    from app.postinfo.routes import postinfo

    app.register_blueprint(auth) 
    app.register_blueprint(postinfo)
    app.register_blueprint(mail)
    app.register_blueprint(payment)

    return app 

