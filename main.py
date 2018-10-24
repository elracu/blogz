
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogzpassword@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

#Class that will be used to generate blog info in the database

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

#Class that will be used to generate user info in the database

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            # TODO - "remember" that user has logged in
            return redirect('/newpost')
        else:
            # TODO - explain login failed
            return '<h1>Error!</h1>'




    return render_template('login.html')


@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verifypassword = request.form['verifypassword']

        invalid_username_error = ''
        invalid_password_error = ''
        verify_error = ''
        # duplicate_error = ''

        #validating username
        if not(3 <= len(username) <=20) or (' ' in username) == True:
            invalid_username_error = "That's not valid username"
            username = ''

        else:
            username = username

        #validating password
        if not(3 <= len(password) <=20) or (' ' in password) == True:
            invalid_password_error = "That's not valid password"

        #validating password verification
        if password != verifypassword:
            verify_error = "Passwords don't match"

        existing_user = User.query.filter_by(username=username).first()
        

        if not existing_user and not invalid_username_error and not invalid_password_error and not verify_error:
            
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            return redirect ('/newpost')
            #TODO - "remember" that user has logged in 
            

        else:
            invalid_username_error = "A user with that username already exists"
            return render_template('signup.html',invalid_username_error = invalid_username_error, invalid_password_error = invalid_password_error,
            verify_error = verify_error, username = username)

    return render_template('signup.html')


@app.route('/', methods=['POST','GET'])
@app.route('/blog', methods=['POST','GET'])
def index():
    #defines a variable that will hold the unique id for each entry
    entryid = request.args.get('id')

    # if a user has clicked on one of the blog entry titles and passed on an id this executes
    if (entryid):
        entry = Blog.query.get(entryid)
        #renders the individual_entry template
        return render_template('individual_entry.html', title="Blog Entry", entry=entry)

    else:
        entries = Blog.query.all()

    return render_template('blog.html', title="Build A Blog", entries=entries)

# @app.route('/blog', methods=['POST','GET'])
# def blog():

#     entries = Blog.query.all()

#     return render_template('blog.html', title="Build A Blog", entries=entries)


@app.route('/newpost', methods=['POST','GET'])
def newpost():

    #check if a request is coming in, if not just render the empty form

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        invalid_blog_title_error = ''
        invalid_blog_body_error = ''

        #validating title
        if title == '':
            invalid_blog_title_error = "Please fill in the title"

        else:
            title = title

        #validating body
        if body == '':
            invalid_blog_body_error = "Please fill in the body"

        else:
            body = body

        #global check on title and body
        
        if not invalid_blog_title_error and not invalid_blog_body_error: 

            new_entry = Blog(title,body,owner)
            db.session.add(new_entry)
            db.session.commit()

            # entries = Blog.query.all() 

            # return render_template('blog.html', title="Build A Blog", entries=entries)

            return redirect('/blog?id=' + str(new_entry.id))

        else:
            return render_template('newpost.html',invalid_blog_title_error = invalid_blog_title_error, invalid_blog_body_error = invalid_blog_body_error, title = title, body = body)

    #render the empyt form
    else:
        return render_template('newpost.html')


@app.route('/individualentry')
def individualentry():
    title = request.args['title']
    body = request.args['body']
    return title + body


if __name__ == '__main__':
    app.run()

