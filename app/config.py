import os
import stripe

# This gives me the filename which is represented by __file__ path as an absolute import. 
#basedir_for_uploads = os.path.abspath(os.path.profilepictures(__file__))

# This gives me the path to the folder that this file is in. This is an absolute import. 
# example below
# C:\Users\username\OneDrive\Desktop\flaskcodeusethis\flaskblog2\app
basedir_for_database = os.path.abspath(os.path.dirname(__file__))



# what is object ?
class Config(object): 
    TESTING = False
    # Setup CSRF secret key
    # change to environment variable todo!
    SECRET_KEY = 'temp_secret_key'
    # this is the test key for stripe 
    stripe.api_key = os.environ['STRIPE_SECRET_KEY']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # DATABASE_URI = sqlite:///app.db,  enviroment variable
    # 'sqlite:///' and os.path.join(basedir, 'app.db') = sqlite:///C:\Users\user\OneDrive\Desktop\flaskcodeusethis\flaskblog2\app\app.db
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
    'sqlite:///' + os.path.join(basedir_for_database, 'app.db')   
    ''' Database For pytesting'''
    # Test_DATABASE_URI = sqlite:///test_app.db.
    # 'sqlite:///' and os.path.join(basedir, 'test_app.db') = sqlite:///C:\Users\user\OneDrive\Desktop\flaskcodeusethis\flaskblog2\app\test_app.db
    Test_DATABASE_URI = os.environ.get('Test_DATABASE_URI') or \
    'sqlite:///' + os.path.join(basedir_for_database, 'test_app.db')
    # for 2+ databases
    SQLALCHEMY_BINDS = { "testing_app_db": Test_DATABASE_URI }
    # setting up Outlook email for flask-redmail
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT  = 587

class DevelopmentConfig(Config):
    '''app.config['SECRET_KEY'] ,is removed in the class config's and becomes just SECRET_KEY'''
    
    # should it be False? NO.
    DEBUG = True
    #  for pytest?
    TESTING = True
    
    # need this to prevent error in redmail. 
    SECURITY_EMAIL_SENDER = "no-reply@example.com"
    # This will be the same value as ['DEBUG'] = ... 
    Mail_DEBUG = True  
    # This is the default email that you get when you send an email?
    MAIL_DEFAULT_SENDER = None  
    # You can only send x amount of emails at one time. Can also be set to None.
    MAIL_MAX_EMAILS = 5  
    # same value ['TESTING'] =. If you are testing your app if you don't want to send emails make it True?
    # ['MAIL_SUPRESS_SEND'] = False 
    # converts the file name to ascii. ascii characters are english characters. (Why use this?)
    MAIL_ASCII_ATTACHMENTS = False 
    #Todo change to env variable so it is not shown change.
    UPLOAD_FOLDER = r"C:\Users\nmyle\OneDrive\Desktop\flaskcodeusethis\flaskblog2\app\static\profilepictures"
    # max a file can be is 1 megabyte is that big enough? Todo add warning
    MAX_CONTENT_LENGTH = 1024 * 1024
    
    
    CKEDITOR_PKG_TYPE = 'standard'

    #EMAIL_USERNAME = os.environ['EMAIL_USERNAME']
    #EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']


    from redmail import gmail
    # setting up gmail  for flask-redmail
    gmail.username = os.environ['EMAIL_USERNAME']
    gmail.password = os.environ['EMAIL_PASSWORD']

    # This is for  flask-mail
    # connect to your mail server not your email address
    # confused by localhost
    # MAIL_SERVER = 'localhost'


    # setting UP Outlook email for flask-redmail
    
    #from redmail import outlook
    #outlook.username = os.environ['EMAIL_USERNAME']
    #outlook.password  = os.environ['EMAIL_PASSWORD']
    #EMAIL_HOST = 'smtp.office365.com'
    #EMAIL_PORT = '587'    
    
    '''
    #depends on email provider
    MAIL_PORT =  None 
    # used for security purposes depend on email provider
    
    MAIL_USE_TLT = False
    MAIL_USE_SSL = False 
    ''' 
    '''
    # username of the linked mail account  
    MAIL_USERNAME = None
    # password of the linked mail account
    MAIL_PASSWORD = None
    '''
    WTF_CSRF_ENABLED = True

class PytestConfig(Config): 
    DEBUG = False
    EMAIL_HOST = 'localhost'
   
    Mail_DEBUG = True  
    # for pytest?
    TESTING = True	   
    # This is the same value ['TESTING'] =...
    # If you are testing your app and you don't want to send emails make the value True?
    MAIL_SUPRESS_SEND = True  
    # When this is False wtf_forms is disabled. This makes 'POST' request work for pytest when False.
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True 
 
    #SERVER_NAME = 'localhost'



"""
class PostPytestConfig(Config): 
''' This is needed if I want to use Post request in pytest because blocks Post request requires form.crsf_token '''    
    # When False this disables wtf forms. This makes POST request work for pytest when False.
    WTF_CSRF_ENABLED = False
    TESTING = True	
    #Debug needs to = False or I will get an error caused by create_all(...) vs delete_all(...).
    DEBUG = False
"""


 

