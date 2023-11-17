# flaskblog #
## Here is a blog built using flask ##


## Here is how you install flaskblog in Visual Studio Code. ##

1. Clone the project
2. Create the environment variables.
3. Install python and conda and import the environment.yml file. Also in VSC download the python extension and setup the conda env.
4. create the db by following the link here [https://flask-migrate.readthedocs.io/en/latest/]
5. To run the code in the CLI follow this link [https://flask.palletsprojects.com/en/2.3.x/cli/] 

For example on windows and powershell in VSC type 

> $env:FLASK_DEBUG='True'              
> $env:FLASK_ENV='dev'
> flask --app app run

6. To run pytest on windows and powershell in VSC type    
> $env:FLASK_ENV='test'      
> pytest -q --capture=no  

## There are a few bugs and minor errors. I am fixing them and I cleaning up the code I also need to add css and improve the html. ##