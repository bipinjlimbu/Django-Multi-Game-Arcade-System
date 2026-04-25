from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import Leaderboard, Game
import json

def guess_view(request):
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
                if score < leaderboard.score: 
                    leaderboard.score = score
                    leaderboard.save()
            
            messages.success(request, 'Your score has been saved to the leaderboard!')
            return redirect('/games/number-guess/')
            
        except json.JSONDecodeError:
            messages.error(request, 'Invalid JSON received')
            return redirect('/games/number-guess/')

    return render(request, 'games/guess_game.html')

def reaction_view(request):
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
                if score > leaderboard.score:
                    leaderboard.score = score
                    leaderboard.save()
            
            messages.success(request, 'Your score has been saved to the leaderboard!')
            return redirect('/games/reaction-game/')
            
        except json.JSONDecodeError:
            messages.error(request, 'Invalid JSON received')
            return redirect('/games/reaction-game/')
        
    return render(request, 'games/reaction_game.html')

def memory_view(request):
    return render(request, 'games/memory_game.html')