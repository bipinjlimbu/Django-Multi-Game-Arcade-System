from django.shortcuts import render
from ..models import Leaderboard, Game, QuizCategory

def home_view(request):
    return render(request, 'main/home_page.html')

def games_view(request):
    games = Game.objects.all()
    return render(request, 'main/games_page.html', {'games': games})

def leaderboard_selection_view(request):
    games = Game.objects.all()
    return render(request, 'main/leaderboard_selection_page.html', {'games': games})

def leaderboard_view(request, game_slug):
    game = Game.objects.get(slug=game_slug)
    if game.name == 'Number Guess' or game.name == 'Memory Game':
        players = Leaderboard.objects.filter(game=game).order_by('score')
        
    elif game.name == 'Reaction Game' or game.name == 'Math Challenge':
        players = Leaderboard.objects.filter(game=game).order_by('-score')
        
    elif game.slug == 'quiz':
        category_slug = request.GET.get('category')
        if category_slug:
            category = QuizCategory.objects.get(slug=category_slug)
            players = Leaderboard.objects.filter(game=game, quiz_category=category).order_by('-score')
        else:
            categories = QuizCategory.objects.all()
            return render(request, 'main/quiz_leaderboard_page.html', {'categories': categories})
        
    return render(request, 'main/leaderboard_page.html', {'game': game, 'players': players})
    