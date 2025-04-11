from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html', title='Inicio')

@bp.route('/posts')
def posts():
    return render_template('posts.html', title='Publicaciones')
