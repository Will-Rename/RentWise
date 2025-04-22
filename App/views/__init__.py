# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
from .admin import setup_admin
from .reviews import reviews_views

views = [user_views, index_views, auth_views, reviews_views] 
# blueprints must be added to this list