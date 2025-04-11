import requests
from requests.exceptions import RequestException
from slugify import slugify

def generate_slug(title, existing_slugs=None):
    if existing_slugs is None:
        existing_slugs = []
    
    base_slug = slugify(title)
    slug = base_slug
    counter = 1
    
    while slug in existing_slugs:
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    return slug

def migrate_slugs():
    try:
        # Obtener todos los posts
        response = requests.get('http://localhost:8000/api/v1/posts')
        response.raise_for_status()
        posts = response.json()
        
        # Obtener slugs existentes
        existing_slugs = [post.get('slug') for post in posts if post.get('slug')]
        
        # Actualizar posts sin slug
        for post in posts:
            if not post.get('slug'):
                slug = generate_slug(post['title'], existing_slugs)
                existing_slugs.append(slug)
                
                # Actualizar el post con el nuevo slug
                update_response = requests.patch(
                    f'http://localhost:8000/api/v1/posts/{post["id"]}',
                    json={'slug': slug}
                )
                update_response.raise_for_status()
                print(f"Generado slug '{slug}' para el post '{post['title']}'")
        
        print("Migración completada exitosamente")
        
    except RequestException as e:
        print(f"Error durante la migración: {str(e)}")

if __name__ == '__main__':
    migrate_slugs() 