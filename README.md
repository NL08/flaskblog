## flaskblog ##
# Here is a blog built using flask #


# Here is how you install flaskblog in Visual Studio Code. #

1. Clone the project
2. Create the environment variables.
3. Install python and conda and import the conda env. Also in VSC download the python extension and setup the conda env.
4. create the db by follwing the link here [https://flask-migrate.readthedocs.io/en/latest/]
5. To run the code in the CLI follow this link [https://flask.palletsprojects.com/en/1.1.x/cli/] 

For example on windows in VSC type in terminal

> $env:FLASK_APP="wsgi"    
> g$env:FLASK_ENV="development"      
> flask run 
6. To run pytest on windows in VSC type 

> $env:FLASK_APP="wsgi"    
> g$env:FLASK_ENV="pytest"      
> pytest -q --capture=no  

# There are a few bugs and minor errors. I am fixing them and I cleaning up the code. # 