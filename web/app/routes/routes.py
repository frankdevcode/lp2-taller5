from flask import Blueprint, render_template, redirect, url_for
from models.post import Post

main_routes = Blueprint('main', __name__)

@main_routes.route('/posts')
def posts():
  posts = Post.query.all()
  return render_template('posts.html', posts=posts, title='Publicaciones')

@main_routes.route('/post/<int:post_id>')
def post_redirect(post_id):
  # Redirección para mantener compatibilidad con URLs antiguas
  post = Post.query.get_or_404(post_id)
  return redirect(url_for('main.post', slug=post.slug), code=301)

@main_routes.route('/post/<slug>')
def post(slug):
  post = Post.query.filter_by(slug=slug).first_or_404()
  return render_template('post.html', post=post, title=post.title)