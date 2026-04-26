from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import Leaderboard, Game, QuizCategory
import json

def game_view(request, game_slug):
    game = Game.objects.get(slug=game_slug)
    
    if game.name == 'Quiz Game':
        categories = QuizCategory.objects.all()
        return render(request, 'quiz_selection_page.html', {'categories': categories})
    
    return render(request, f'games/{game_slug}.html', {'game': game})

def save_score(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            slug = data.get('slug')
            score = data.get('score')
            game = Game.objects.get(slug=slug)
                    
            if not Leaderboard.objects.filter(user = request.user, game=game).exists():
                leaderboard = Leaderboard.objects.create(user=request.user, score=score, game=game)
                leaderboard.save()
                
            else:
                leaderboard = Leaderboard.objects.get(user=request.user, game=game)
                if (game.name == 'Number Guess' or game.name == 'Memory Game') and score < leaderboard.score:
                    leaderboard.score = score
                    leaderboard.save()
                    
                elif (game.name == 'Reaction Game' or game.name == 'Math Challenge') and score > leaderboard.score:
                    leaderboard.score = score
                    leaderboard.save()

            messages.success(request, 'Your score has been saved to the leaderboard!')
            return redirect(f'/games/{slug}/')
            
        except json.JSONDecodeError:
            messages.error(request, 'Invalid JSON received')
            return redirect(f'/games/{slug}/')

    return redirect(f'/games/{slug}/')