from django.shortcuts import render, redirect
import json

def guess_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('game_name')
            score = data.get('score')
            print(f"Received score for {name}: {score}")
        except json.JSONDecodeError:
            print("Invalid JSON received")
            return redirect('guess')
        return redirect('guess')
    return render(request, 'games/guess_game.html')