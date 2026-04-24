from django.urls import path
from .views.auth_view import register_view, logout_view
from .views.main import home_view, games_view

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('games/', games_view, name='games'),
]