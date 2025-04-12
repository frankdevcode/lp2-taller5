from flask import Blueprint, render_template, abort
import requests

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    try:
        response = requests.get('http://api:5000/api/v1/posts')
        posts = response.json() if response.status_code == 200 else []
    except requests.RequestException:
        posts = []
    
    meta = {
        'title': 'Blog Personal',
        'description': 'Blog de ejemplo usando Flask y FastAPI',
        'keywords': 'blog, flask, fastapi, python',
        'author': 'Mi Nombre',
        'og_url': '/',
        'og_title': 'Blog Personal',
        'og_description': 'Blog de ejemplo usando Flask y FastAPI',
        'og_image': '/static/img/og-image.jpg',
        'twitter_card': 'summary_large_image',
        'twitter_site': '@miusuario'
    }
    
    return render_template('blog/index.html', posts=posts, meta=meta)

@bp.route('/post/<int:post_id>')
def post_detail(post_id):
    try:
        response = requests.get(f'http://api:5000/api/v1/posts/{post_id}')
        if response.status_code != 200:
            abort(404)
        post = response.json()
    except requests.RequestException:
        abort(500)
    
    meta = {
        'title': post.get('title', 'Post sin título'),
        'description': post.get('content', '')[:160] + '...',
        'keywords': 'blog, post, detalle',
        'author': post.get('author', {}).get('username', 'Autor desconocido'),
        'og_url': f'/post/{post_id}',
        'og_title': post.get('title', 'Post sin título'),
        'og_description': post.get('content', '')[:160] + '...',
        'og_image': post.get('image_url', '/static/img/og-image.jpg'),
        'twitter_card': 'summary_large_image',
        'twitter_site': '@miusuario'
    }
    
    return render_template('blog/post_detail.html', post=post, meta=meta)