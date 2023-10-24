from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.models import Posts, User
from app.postinfo.forms import Emptyform, Postform

# make @postinfo work from postinfo folder
postinfo = Blueprint('postinfo', __name__, template_folder='templates')


@postinfo.route("/post/new", methods = ['POST', 'GET'])
@login_required
# I need to link to the name of the function in the html. Ex new_post 
def new_post(): 
    form = Postform()
    if form.validate_on_submit():
        title_form = form.title.data
        content_form = form.content.data
        date_posted_form = datetime.now()
        # user.id is the foreign key in the Post database. You need to manually add FK's.   
        # The foreignkey "user_id = db_post.post.id", "db_post.post.id is equal to the id in User table.
        user_db = User.query.filter_by(username=current_user.username).first()
        user_db_id = user_db.id
        posts = Posts(title=title_form, content=content_form, date_posted=date_posted_form, fk_user_id=user_db_id )  
        db.session.add(posts)  
        db.session.commit()

 
        # redirect to the post after complete because you want to see the posted post. 
        # Also redirecting to home won't work because I need to pass on post_id. 
          
        flash('You have posted successfully') 
        #post_db = Posts.query.filter_by(title=title_form).first()
        #post_id = post_db.id
        #return redirect(url_for('postinfo.post', post_id))
        return redirect('auth.home')
    return render_template('new_post.html',title='new post', form=form)



# gives you the ability to click on posts from /home route and see the posts
# create the post/number route
# gets the posts number
@postinfo.route("/post/<int:post_id>", methods = ['POST', 'GET'])
def post(post_id):
    # Pass on the Posts database to the post_number variable. If the post doesn't exist get 404 error
    # The reason I don't use posts.id is because I want a certain "Posts database id". 
    
    post = Posts.query.get_or_404(post_id)
    post_id = post.id
    form = Emptyform()    
    # Do I need to pass on post_id 
    return render_template('post.html', post=post, post_id=post_id, title='post', form=form)





# The reason you have post_id is because you only want to edit 1 post at a time. 
# If you leave out post_id you would edit every posts. 
@postinfo.route("/post/edit/<int:post_id>", methods = ['POST', 'GET'])
# edit/update posts
@login_required
def edit_post(post_id): 
    # get request
    post_db = Posts.query.get_or_404(post_id) 
    form = Postform()
    if form.validate_on_submit():
        # delete the current columns in db
        delete_post = post_db
         
        db.session.delete(delete_post)  
        db.session.commit()
        # add/edit the current forms in the db
        title_form = form.title.data
        content_form = form.content.data 
        posts = Posts(title=title_form, content=content_form ,user_id=current_user.id)
        db.session.add(posts)  
        db.session.commit()
        flash('You have edited your post successfully')
        return redirect(url_for('auth.home'))

    elif request.method == 'GET':        
        # this makes the forms have the value from the db show up when you edit the forms 
        # for this to work all you have to do is pass on form.
        post_title_db = post_db.title
        post_content_db = post_db.content
        # put this below the if statement so ex "form.title.data" doesn't interfere with above ex "form.title.date
        form.title.data =  post_title_db 
        form.content.data = post_content_db
        return render_template('edit_post.html', title='edit post', form=form) 






# Can I go ("/post/<int:post_id>/delete") instead of below? No
@postinfo.route("/post/delete/<int:post_id>", methods = ['POST'])
@login_required
def delete_post(post_id): 
    if request.method == 'POST':       
        post_db = Posts.query.get_or_404(post_id)   
        delete_post = post_db
        db.session.delete(delete_post)
        db.session.commit()
        flash('You have deleted your post')
         # can someone input a fake post to delete?

        # You don't want post.html because that is the individual post.
        return redirect(url_for('auth.home'))
    





















