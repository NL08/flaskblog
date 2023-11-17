from app import create_app
app = create_app()

from app.main.forms import SearchForm
@app.context_processor
def layout():
    '''
    Pass Stuff to Navbar such as a form in layout.html from search.html
        
    If I don't pass on the form in base function then I will 
    get an error in layout.html because of {{form.csrf_token}} 
    ''' 
    form = SearchForm()
    return dict(form=form) 
 
 

 

 