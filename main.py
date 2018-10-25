
from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogzpassword@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
app.secret_key = 'dfja9afn3290akdsf'

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

# check for login - run the function before moving on to incoming request
@app.before_request
def require_login():
    allowed_routes = ['login','signup','index', 'list_blogs']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect ('/login')



@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        invalid_username_error = ''
        invalid_password_error = ''

        #validating username
        if not user:
            invalid_username_error = 'Invalid username'

        #validating password
        if password == '' or user.password != password: 
            invalid_password_error = 'Invalid password'

        if user and user.password == password:
            session['username']=username # user has logged in session has been created
            return redirect('/newpost')

        else:
            return render_template('login.html', invalid_username_error = invalid_username_error, invalid_password_error = invalid_password_error)

    return render_template('login.html')


@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verifypassword = request.form['verifypassword']
        existing_user = User.query.filter_by(username=username).first()

        invalid_username_error = ''
        invalid_password_error = ''
        verify_error = ''
        duplicate_error = ''

        #validating username
        if not(3 <= len(username) <=20) or (' ' in username) == True:
            invalid_username_error = "That's not valid username"
            username = ''

        #validating password
        if not(3 <= len(password) <=20) or (' ' in password) == True:
            invalid_password_error = "That's not valid password"

        #validating password verification
        if password != verifypassword:
            verify_error = "Passwords don't match"
        
        if existing_user != None:
            duplicate_error = 'That user already exists'

        if not existing_user and not invalid_username_error and not invalid_password_error and not verify_error:
            
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username']=username # user has logged in session has been created 
            return redirect ('/newpost')

        else:
            return render_template('signup.html', invalid_username_error = invalid_username_error, invalid_password_error = invalid_password_error,
            verify_error = verify_error, username = username, duplicate_error = duplicate_error)

    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

@app.route('/', methods=['POST','GET'])
def index():
    users = User.query.all()
    return render_template('index.html', title="Blog Users", users=users)


@app.route('/blog', methods=['POST','GET'])
def list_blogs():
    entryid = request.args.get('id')
    user = request.args.get('user')

    # execute when link/title for enntry has been clicked
    if (entryid):
        entry = Blog.query.get(entryid)
        return render_template('individual_entry.html', title="Blog Entry", entry=entry)

    # execute when link for individual user has been clicked
    if (user):
        entries = Blog.query.filter_by(owner_id=user).all()
        return render_template('user_page.html', entries=entries)

    else:
        entries = Blog.query.all()

    return render_template('blog.html', title="Build A Blog", entries=entries)


@app.route('/newpost', methods=['POST','GET'])
def newpost():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        owner = User.query.filter_by(username=session['username']).first()

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

