from flask import Blueprint, render_template, abort, redirect, url_for, request, flash, current_app, session
import requests
from .auth import login_required
import os
from werkzeug.utils import secure_filename

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

@bp.route('/post/<slug>')
def post_detail(slug):
    try:
        response = requests.get(f'http://api:5000/api/v1/posts/slug/{slug}')
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
        'og_url': f'/post/{slug}',
        'og_title': post.get('title', 'Post sin título'),
        'og_description': post.get('content', '')[:160] + '...',
        'og_image': post.get('image_url', '/static/img/og-image.jpg'),
        'twitter_card': 'summary_large_image',
        'twitter_site': '@miusuario'
    }
    
    return render_template('blog/post_detail.html', post=post, meta=meta)

# Ruta de compatibilidad para IDs
@bp.route('/post/id/<int:post_id>')
def post_detail_by_id(post_id):
    try:
        # Obtener el post por ID
        response = requests.get(f'http://api:5000/api/v1/posts/{post_id}')
        if response.status_code != 200:
            abort(404)
        post = response.json()
        
        # Redirigir a la URL con slug
        return redirect(url_for('blog.post_detail', slug=post['slug']), code=301)
    except requests.RequestException:
        abort(500)

@bp.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        try:
            # Preparar datos del post
            data = {
                'title': request.form['title'],
                'content': request.form['content'],
                'category_id': request.form.get('category_id'),
                'is_draft': bool(request.form.get('draft'))
            }
            
            # Obtener archivo de imagen si existe
            if 'image' in request.files:
                image = request.files['image']
                if image.filename:
                    filename = secure_filename(image.filename)
                    # Guardar imagen y obtener URL
                    image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    image.save(image_path)
                    data['image_url'] = url_for('static', filename=f'uploads/{filename}', _external=True)

            # Enviar datos a la API
            response = requests.post(
                f"{current_app.config['API_URL']}/api/v1/posts",
                json=data,
                headers={'Authorization': f"Bearer {session.get('token')}"}
            )
            
            if response.status_code == 201:
                post = response.json()
                flash('Publicación creada exitosamente', 'success')
                return redirect(url_for('blog.post_detail', slug=post['slug']))
            else:
                flash('Error al crear la publicación', 'danger')
        
        except requests.RequestException as e:
            flash(f'Error al conectar con el servidor: {str(e)}', 'danger')
    
    # Obtener categorías para el formulario
    try:
        categories_response = requests.get(f"{current_app.config['API_URL']}/api/v1/categories")
        categories = categories_response.json() if categories_response.status_code == 200 else []
    except requests.RequestException:
        categories = []
    
    return render_template('blog/post_form.html', categories=categories)

@bp.route('/post/<slug>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(slug):
    # Obtener el post existente
    try:
        response = requests.get(f"{current_app.config['API_URL']}/api/v1/posts/slug/{slug}")
        if response.status_code != 200:
            abort(404)
        post = response.json()
        
        # Verificar permisos
        if post['user_id'] != session.get('user_id') and not session.get('is_admin'):
            abort(403)
        
        if request.method == 'POST':
            # Preparar datos actualizados
            data = {
                'title': request.form['title'],
                'content': request.form['content'],
                'category_id': request.form.get('category_id'),
                'is_draft': bool(request.form.get('draft'))
            }
            
            # Manejar nueva imagen si se proporciona
            if 'image' in request.files:
                image = request.files['image']
                if image.filename:
                    filename = secure_filename(image.filename)
                    image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    image.save(image_path)
                    data['image_url'] = url_for('static', filename=f'uploads/{filename}', _external=True)
            
            # Actualizar post
            update_response = requests.put(
                f"{current_app.config['API_URL']}/api/v1/posts/{post['id']}",
                json=data,
                headers={'Authorization': f"Bearer {session.get('token')}"}
            )
            
            if update_response.status_code == 200:
                flash('Publicación actualizada exitosamente', 'success')
                return redirect(url_for('blog.post_detail', slug=post['slug']))
            else:
                flash('Error al actualizar la publicación', 'danger')
        
        # Obtener categorías para el formulario
        categories_response = requests.get(f"{current_app.config['API_URL']}/api/v1/categories")
        categories = categories_response.json() if categories_response.status_code == 200 else []
        
        return render_template('blog/post_form.html', post=post, categories=categories)
    
    except requests.RequestException as e:
        flash(f'Error al conectar con el servidor: {str(e)}', 'danger')
        return redirect(url_for('blog.index'))

@bp.route('/post/<slug>/delete', methods=['POST'])
@login_required
def delete_post(slug):
    try:
        # Obtener información del post
        response = requests.get(f"{current_app.config['API_URL']}/api/v1/posts/slug/{slug}")
        if response.status_code != 200:
            abort(404)
        post = response.json()
        
        # Verificar permisos
        if post['user_id'] != session.get('user_id') and not session.get('is_admin'):
            abort(403)
        
        # Eliminar post
        delete_response = requests.delete(
            f"{current_app.config['API_URL']}/api/v1/posts/{post['id']}",
            headers={'Authorization': f"Bearer {session.get('token')}"}
        )
        
        if delete_response.status_code == 204:
            flash('Publicación eliminada exitosamente', 'success')
        else:
            flash('Error al eliminar la publicación', 'danger')
            
    except requests.RequestException as e:
        flash(f'Error al conectar con el servidor: {str(e)}', 'danger')
    
    return redirect(url_for('blog.index'))