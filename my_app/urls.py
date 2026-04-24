from django.urls import path
from .views.main import home_view, games_view

urlpatterns = [
    path('', home_view, name='home'),
    path('games/', games_view, name='games'),
]