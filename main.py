
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blogpassword@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

#Class that will store blog info in the database

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)

    def __init__(self, title, body):
        self.title = title
        self.body = body



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

            new_entry = Blog(title,body)
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

# http://127.0.0.1:5000/individualentry?title=hello&body=copy


# @app.route('/individualentry', methods=['POST','GET'])
# def individualentry():

#     entries = Blog.query.all()

#     return render_template('individual_entry.html', title="Individual Entry", entries=entries)

if __name__ == '__main__':
    app.run()

