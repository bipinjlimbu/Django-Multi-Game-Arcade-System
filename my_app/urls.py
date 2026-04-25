from django.urls import path
from .views.auth_view import register_view, login_view, logout_view
from .views.main_view import home_view, games_view, leaderboard_selection_view, leaderboard_view
from .views.game_view import guess_view, reaction_view

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('games/', games_view, name='games'),
    path('leaderboard/', leaderboard_selection_view, name='leaderboard_selection'),
    path('leaderboard/<str:game_slug>/', leaderboard_view, name='leaderboard'),
    path('guess/', guess_view, name='guess'),
    path('reaction/', reaction_view, name='reaction'),
]