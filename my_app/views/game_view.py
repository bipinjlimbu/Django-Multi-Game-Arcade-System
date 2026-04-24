from django.shortcuts import render, redirect

def guess_view(request):
    return render(request, 'games/guess_game.html')