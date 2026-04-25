from django.shortcuts import render
from ..models import Leaderboard, Game

def home_view(request):
    return render(request, 'main/home_page.html')

def games_view(request):
    return render(request, 'main/games_page.html')

def leaderboard_selection_view(request):
    games = Game.objects.all()
    return render(request, 'main/leaderboard_selection_page.html', {'games': games})

def leaderboard_view(request, game_slug):
    game = Game.objects.get(slug=game_slug)
    if game.name == 'Number Guess':
        players = Leaderboard.objects.filter(game=game).order_by('score')
        
    elif game.name == 'Reaction Game':
        players = Leaderboard.objects.filter(game=game).order_by('-score')
        
    return render(request, 'main/leaderboard_page.html', {'game': game, 'players': players})
    