from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import requests
from requests.exceptions import RequestException

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    try:
        response = requests.get('http://localhost:8000/api/v1/posts')
        response.raise_for_status()
        posts = response.json()
    except RequestException as e:
        print(f"Error al obtener posts: {str(e)}")
        posts = []
    return render_template('index.html', posts=posts)

@bp.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@bp.route('/post/<int:post_id>')
def post_redirect(post_id):
    try:
        # Obtener el post por ID
        response = requests.get(f'http://localhost:8000/api/v1/posts/{post_id}')
        response.raise_for_status()
        post = response.json()
        
        # Redirigir a la URL con slug
        return redirect(url_for('main.post', slug=post['slug']), code=301)
    except RequestException as e:
        print(f"Error al obtener post: {str(e)}")
        return render_template('404.html'), 404

@bp.route('/post/<slug>')
def post(slug):
    try:
        # Obtener el post por slug
        response = requests.get(f'http://localhost:8000/api/v1/posts/slug/{slug}')
        response.raise_for_status()
        post = response.json()
    except RequestException as e:
        print(f"Error al obtener post: {str(e)}")
        post = None
    return render_template('post.html', post=post)

@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500