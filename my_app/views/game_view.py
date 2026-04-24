from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import Leaderboard
import json

def guess_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            score = data.get('score')
            
            leaderboard = Leaderboard.objects.create(user=request.user, score=score, game=name)
            leaderboard.save()
            
            messages.success(request, 'Your score has been saved to the leaderboard!')
            return redirect('guess')
            
        except json.JSONDecodeError:
            messages.error(request, 'Invalid JSON received')
            return redirect('guess')

    return render(request, 'games/guess_game.html')

def reaction_view(request):
    return render(request, 'games/reaction_game.html')