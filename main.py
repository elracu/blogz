
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
def index():

    #check the type of request that's coming in. POST or GET

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_entry = Blog(blog_title,blog_body)
        db.session.add(new_entry)
        db.session.commit()

    entries = Blog.query.all()    


    return render_template('blog.html', title="Build A Blog", entries=entries)



if __name__ == '__main__':
    app.run()