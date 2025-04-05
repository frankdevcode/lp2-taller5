from flask import Blueprint, render_template
from models.post import Post

main_routes = Blueprint('main', __name__)

@main_routes.route('/posts')
def posts():
    posts = Post.query.all()
    return render_template('posts.html', posts=posts, title='Publicaciones')

@main_routes.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post, title=post.title)