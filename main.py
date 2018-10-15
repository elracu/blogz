
from flask import Flask, request, redirect, render_template

app = Flask(__name__)
app.config['DEBUG'] = True

titles = []

@app.route('/', methods=['POST','GET'])
def index():

    #check the type of request that's coming in. POST or GET

    if request.method == 'POST':
        title = request.form['title']
        titles.append(title)


    return render_template('blog.html', title="Build A Blog", titles=titles)




app.run()