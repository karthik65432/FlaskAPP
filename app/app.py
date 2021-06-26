from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from model import Blogpost, app, db,User
from datetime import datetime
import pytz


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/posts')
def posts():
    all_posts = Blogpost.query.order_by(Blogpost.date_posted)
    return render_template('posts.html', posts=all_posts)

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = Blogpost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/edit/<int:id>', methods = ['GET','POST'])
def edit(id):
    post = Blogpost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html',post=post)

@app.route('/posts/new', methods = ['GET','POST'])
def newpost():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = Blogpost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('newpost.html')

@app.route('/register', methods = ['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user=User(username=form.username.data,email=form.email.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created successfully for {form.username.data}',category='success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register',form=form)

@app.route('/login', methods = ['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if form.email.data == user.email and form.password.data == user.password:
            flash(f'Login Successful for {form.email.data}', category='success')
            return redirect(url_for('newpost'))
        else:
            flash(f'Login Failed for {form.email.data}', category='danger')
    return render_template('login.html', title='Login',form=form)

if __name__ == '__main__':
    app.run(port=80, host="0.0.0.0", debug=True)
