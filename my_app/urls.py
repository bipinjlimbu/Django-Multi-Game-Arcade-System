from django.urls import path
from .views.auth_view import register_view, login_view, logout_view
from .views.main_view import home_view, games_view, leaderboard_selection_view, leaderboard_view
from .views.game_view import game_view, save_score, quiz_view

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('games/', games_view, name='games'),
    path('leaderboard/', leaderboard_selection_view, name='leaderboard_selection'),
    path('leaderboard/<str:game_slug>/', leaderboard_view, name='leaderboard'),
    path('games/<str:game_slug>/', game_view, name='game_detail'),
    path('save-score/', save_score, name='save_score'),
    path('games/quiz/<str:category_slug>/', quiz_view, name='quiz'),
]