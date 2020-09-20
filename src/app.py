from os import name
from flask import Flask, render_template, request
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#configs
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#models
class BlogPost(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    author = db.Column(db.String(20),nullable=False,default='NA')
    date_created = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post ' + str(self.id)


all_post = [
    {
        'title' : 'post 1',
        'content' : 'this is the content of post 1',
        'author' : 'Edison'
    },
    {
        'title' : 'post 2',
        'content' : 'this is the content of post 2'
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post',methods=['GET','POST'])
def post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title,content = post_content,author=post_author)
        try:
            db.session.add(new_post)
            db.session.commit()
            return redirect('/post')
        except:
            return 'Error while creating new post'
    else:
        all_post = BlogPost.query.order_by('date_created').all()
        return render_template('post.html',posts=all_post)

@app.route('/post/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/post')

@app.route('/post/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id) 
    if request.method == 'POST':       
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/post')
    else:
        return render_template('edit.html',post=post)

@app.route('/home/<string:name>/post/<int:id>')
def hello(id,name):
    return 'hello, ' + name + ' your id is: ' + str(id)

@app.route('/onlyget',methods=['GET'])
def get_req():
    return 'you can only get here'

if __name__ == '__main__':
    app.run(debug=True)