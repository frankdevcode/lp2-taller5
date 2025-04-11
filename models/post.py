from datetime import datetime
from models.database import db
from slugify import slugify

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  slug = db.Column(db.String(100), unique=True, nullable=False)
  content = db.Column(db.Text, nullable=False)
  date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  
  def __init__(self, *args, **kwargs):
    super(Post, self).__init__(*args, **kwargs)
    if not self.slug and self.title:
      self.slug = self.generate_slug()
  
  def generate_slug(self):
    base_slug = slugify(self.title)
    slug = base_slug
    counter = 1
    while Post.query.filter_by(slug=slug).first() is not None:
      slug = f"{base_slug}-{counter}"
      counter += 1
    return slug
  
  def __repr__(self):
    return f"Post('{self.title}', '{self.date_posted}')"