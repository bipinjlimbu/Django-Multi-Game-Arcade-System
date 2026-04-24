from django.urls import path
from .views.auth_view import register_view, login_view, logout_view
from .views.main import home_view, games_view, leaderboard_view
from .views.game_view import guess_view

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('games/', games_view, name='games'),
    path('leaderboard/<str:game_name>/', leaderboard_view, name='leaderboard'),
    path('guess/', guess_view, name='guess'),
]