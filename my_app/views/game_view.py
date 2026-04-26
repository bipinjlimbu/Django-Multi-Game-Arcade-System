from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from ..models import Leaderboard, Game, QuizCategory, Question, Option
from django.http import JsonResponse
import json

def game_view(request, game_slug):
    game = Game.objects.get(slug=game_slug)
    
    if game.slug == 'quiz':
        categories = QuizCategory.objects.all()
        return render(request, 'games/quiz_selection_page.html', {'categories': categories})
    
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

def quiz_view(request, category_slug):
    category = get_object_or_404(QuizCategory, slug=category_slug)
    return render(request, 'games/quiz_page.html', {'category': category})

def get_quiz_questions(request, category_slug, level):
    questions = Question.objects.filter(
        category__slug=category_slug, 
        level=level
    ).order_by('?')[:10]
    
    data = []
    for q in questions:
        options = []
        for opt in q.options.all():
            options.append({
                'text': opt.text,
                'is_correct': opt.is_correct
            })
        
        data.append({
            'question': q.text,
            'options': options
        })
    
    return JsonResponse({'questions': data})