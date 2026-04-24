from django.shortcuts import render

def home_view(request):
    return render(request, 'main/home_page.html')

def games_view(request):
    return render(request, 'main/games_page.html')

def leaderboard_view(request, game_name):
    return render(request, 'main/leaderboard_page.html', {'game_name': game_name})
    