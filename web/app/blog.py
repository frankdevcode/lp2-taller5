from flask import Blueprint, render_template
import requests

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    try:
        response = requests.get('http://api:8000/api/v1/posts')
        posts = response.json() if response.status_code == 200 else []
    except requests.RequestException:
        posts = []
    
    meta = {
        'description': 'Blog de ejemplo usando Flask y FastAPI'
    }
    
    return render_template('blog/index.html', posts=posts, meta=meta)