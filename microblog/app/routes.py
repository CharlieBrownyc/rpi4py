from flask import render_template
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was amazing!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('index')
    return render_template('login.html', title='Sign In', form=form)
@app.route('/user/<username>')
def user(username):
    user = {'username': username}
    return render_template('user.html', user=user)
@app.route('/logout')
def logout():
    # Log out user
    flash('User logged out')
    return redirect(url_for('index'))
@app.errorhandler(404)
@app.route('/<path:path>')
@app.route('/404')
def page_not_found(path):
    return render_template('404.html'), 404
@app.route('/403')

    
#     return '''
# <html>
#     <head>
#     <title>Home Page - Microblog</title>
#     </head>
#     <body>
#         <h1>Hello, ''' + user['username'] + '''!</h1>
#     </body>
# </html>
# '''