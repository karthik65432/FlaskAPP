from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)


class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime(), nullable=False, default=datetime.now(pytz.timezone('Asia/Kolkata')))

    def __repr__(self):
        return 'Blog post ' + str(self.id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts', methods = ['GET','POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        new_post = Blogpost(title = post_title, content = post_content)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = Blogpost.query.order_by(Blogpost.date_posted)
        return render_template('posts.html', posts=all_posts)

@app.route('/home/<string:name>')
def hello(name):
    return 'Hello, ' + name


if __name__ == '__main__':
    app.run(debug=True)
