from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import requests
from functools import wraps

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

def admin_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session or not session.get('is_admin'):
            flash('No tienes permiso para acceder a esta página.', 'danger')
            return redirect(url_for('blog.index'))
        return view(**kwargs)
    return wrapped_view

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        error = None

        if not username:
            error = 'El nombre de usuario es obligatorio.'
        elif not email:
            error = 'El correo electrónico es obligatorio.'
        elif not password:
            error = 'La contraseña es obligatoria.'
        elif password != confirm_password:
            error = 'Las contraseñas no coinciden.'

        if error is None:
            try:
                response = requests.post('http://api:5000/api/v1/users', json={
                    'username': username,
                    'email': email,
                    'password': password
                })
                
                if response.status_code == 201:
                    flash('¡Usuario registrado con éxito! Ahora puedes iniciar sesión.', 'success')
                    return redirect(url_for('auth.login'))
                else:
                    error_data = response.json()
                    error = error_data.get('detail', 'Error al registrar el usuario.')
            except requests.RequestException as e:
                error = f"Error al conectar con la API: {str(e)}"

        flash(error, 'danger')

    meta = {
        'title': 'Registro de Usuario - Blog Personal',
        'description': 'Regístrate para crear tu cuenta y publicar en nuestro blog.',
        'keywords': 'registro, usuario, cuenta, blog',
        'author': 'Blog Personal',
        'og_url': '/auth/register',
        'og_title': 'Registro de Usuario - Blog Personal',
        'og_description': 'Regístrate para crear tu cuenta y publicar en nuestro blog.',
        'og_image': '/static/img/og-image.jpg',
        'twitter_card': 'summary_large_image',
        'twitter_site': '@miusuario'
    }
    
    return render_template('auth/register.html', meta=meta)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'El nombre de usuario es obligatorio.'
        elif not password:
            error = 'La contraseña es obligatoria.'

        if error is None:
            try:
                response = requests.post('http://api:5000/api/v1/auth/login', data={
                    'username': username,
                    'password': password
                })
                
                if response.status_code == 200:
                    token_data = response.json()
                    
                    # Obtener información del usuario
                    user_response = requests.get(
                        'http://api:5000/api/v1/users/me',
                        headers={'Authorization': f"Bearer {token_data['access_token']}"}
                    )
                    
                    if user_response.status_code == 200:
                        user_data = user_response.json()
                        
                        # Guardar información en la sesión
                        session['user_id'] = user_data['id']
                        session['username'] = user_data['username']
                        session['is_admin'] = user_data['is_admin']
                        session['token'] = token_data['access_token']
                        
                        flash(f'Bienvenido {user_data["username"]}!', 'success')
                        return redirect(url_for('blog.index'))
                    else:
                        error = 'Error al obtener información del usuario.'
                else:
                    error_data = response.json()
                    error = error_data.get('detail', 'Error de autenticación.')
            except requests.RequestException as e:
                error = f"Error al conectar con la API: {str(e)}"

        flash(error, 'danger')

    meta = {
        'title': 'Iniciar Sesión - Blog Personal',
        'description': 'Inicia sesión para acceder a tu cuenta y gestionar tus publicaciones.',
        'keywords': 'login, iniciar sesión, cuenta, blog',
        'author': 'Blog Personal',
        'og_url': '/auth/login',
        'og_title': 'Iniciar Sesión - Blog Personal',
        'og_description': 'Inicia sesión para acceder a tu cuenta y gestionar tus publicaciones.',
        'og_image': '/static/img/og-image.jpg',
        'twitter_card': 'summary_large_image',
        'twitter_site': '@miusuario'
    }
    
    return render_template('auth/login.html', meta=meta)

@bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('blog.index'))

@bp.route('/profile')
@login_required
def profile():
    try:
        response = requests.get(
            f'http://api:5000/api/v1/users/{session["user_id"]}',
            headers={'Authorization': f"Bearer {session['token']}"}
        )
        
        if response.status_code == 200:
            user = response.json()
        else:
            flash('Error al cargar el perfil.', 'danger')
            user = None
    except (requests.RequestException, KeyError) as e:
        flash(f'Error: {str(e)}', 'danger')
        user = None
    
    meta = {
        'title': 'Mi Perfil - Blog Personal',
        'description': 'Gestiona tu información de perfil y configuraciones de cuenta.',
        'keywords': 'perfil, usuario, cuenta, blog',
        'author': 'Blog Personal',
        'og_url': '/auth/profile',
        'og_title': 'Mi Perfil - Blog Personal',
        'og_description': 'Gestiona tu información de perfil y configuraciones de cuenta.',
        'og_image': '/static/img/og-image.jpg',
        'twitter_card': 'summary_large_image',
        'twitter_site': '@miusuario'
    }
    
    return render_template('auth/profile.html', user=user, meta=meta) 