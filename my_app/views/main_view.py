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
    if game.slug == 'number-guess' or game.slug == 'memory-game':
        players = Leaderboard.objects.filter(game=game).order_by('score')
        
    elif game.slug == 'reaction-game' or game.slug == 'math-challenge' or game.slug == 'arrow-defense' or game.slug == 'whack-a-mole' or game.slug == 'memory-flash-number' or game.slug == 'odd-one-out' or game.slug == 'rock-paper-scissors' or game.slug == 'pattern-memory' or game.slug == 'sequence-rush' or game.slug == 'sliding-puzzle':
        players = Leaderboard.objects.filter(game=game).order_by('-score')
        
    elif game.slug == 'quiz':
        category_slug = request.GET.get('category') if request.GET.get('category') else None
        if category_slug:
            category = QuizCategory.objects.get(slug=category_slug)
            players = Leaderboard.objects.filter(game=game, quiz_category=category).order_by('-score')
        else:
            categories = QuizCategory.objects.all()
            return render(request, 'main/quiz_leaderboard_page.html', {'categories': categories})
        
    return render(request, 'main/leaderboard_page.html', {'game': game, 'players': players})
    