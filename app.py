"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "blog-blog-blog"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def get_homepage():
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('index.html', posts=posts)

@app.route('/users')
def list_users():
    users=User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def new_user():
    return render_template('new_user.html')

@app.route('/users/new', methods=['POST'])
def add_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    image_url = image_url if image_url else None

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/users/{new_user.id}')

@app.route('/users/<int:user_id>')
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    posts = user.posts
    return render_template('user_detail.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def user_edit(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def user_update(user_id):
    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    image_url = request.form['image_url']
    user.image_url = image_url if image_url else None
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def user_delete(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

@app.route('/posts')
def show_all_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('posts.html', posts=posts)

@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('new_post.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    title = request.form['title']
    content = request.form['content']
    tags_id_list = request.form.getlist('tag')

    tag_list = [Tag.query.get(tag_id) for tag_id in tags_id_list]

    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    new_post.tags = tag_list
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    user = post.user
    return render_template('post_detail.html', user=user, post=post)

@app.route('/posts/<int:post_id>/edit')
def post_edit(post_id):
    post = Post.query.get_or_404(post_id)
    user = post.user
    tags = Tag.query.all()
    return render_template('post_edit.html', user=user, post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    tags_id_list = request.form.getlist('tag')
    tag_list = [Tag.query.get(tag_id) for tag_id in tags_id_list]

    post.title = request.form['title']
    post.content = request.form['content']
    post.tags = tag_list
    db.session.commit()

    return redirect(f'/users/{post.user_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    user_id=post.user_id
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/tags')
def all_tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/new')
def new_tag():
    posts = Post.query.all()
    return render_template('new_tag.html', posts=posts)

@app.route('/tags/new', methods=["POST"])
def add_tag():
    name = request.form['name']
    posts_id_list = request.form.getlist('post')
    post_list = [Post.query.get(post_id) for post_id in posts_id_list]

    new_tag = Tag(name=name)
    new_tag.posts = post_list
    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>')
def tag_detail(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts
    return render_template('tag_detail.html', tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit')
def tag_edit(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tag_edit.html', tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def tag_update(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts_id_list = request.form.getlist('post')
    post_list = [Post.query.get(post_id) for post_id in posts_id_list]

    tag.name = request.form['name']
    tag.posts = post_list
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def tag_delete(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')