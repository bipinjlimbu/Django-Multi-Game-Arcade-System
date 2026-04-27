from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from ..models import Leaderboard, Game, QuizCategory, Question, Option
from django.http import JsonResponse
import json
import random

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
            category = data.get('category')
            game = Game.objects.get(slug=slug)
            
            print(f"Received score: {score} for game: {slug} and category: {category} from user: {request.user.username}")
            
            if game.slug == 'quiz':
                quiz_category = QuizCategory.objects.get(slug=category)
                if not Leaderboard.objects.filter(user=request.user, game=game, quiz_category=quiz_category).exists():
                    leaderboard = Leaderboard.objects.create(user=request.user, score=score, game=game, quiz_category=quiz_category)
                    leaderboard.save()
                else:
                    leaderboard = Leaderboard.objects.get(user=request.user, game=game, quiz_category=quiz_category)
                    if score > leaderboard.score:
                        leaderboard.score = score
                        leaderboard.save()
                        
            else:
                if not Leaderboard.objects.filter(user = request.user, game=game).exists():
                    leaderboard = Leaderboard.objects.create(user=request.user, score=score, game=game)
                    leaderboard.save()
                    
                else:
                    leaderboard = Leaderboard.objects.get(user=request.user, game=game)
                    if (game.slug == 'number-guess' or game.slug == 'memory-game') and score < leaderboard.score:
                        leaderboard.score = score
                        leaderboard.save()
                        
                    elif (game.slug == 'reaction-game' or game.slug == 'math-challenge' or game.slug == 'arrow-defense' or game.slug == 'whack-a-mole') and score > leaderboard.score:
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
    questions_qs = Question.objects.filter(
        category__slug=category_slug, 
        level=level
    ).order_by('?')[:10]
    
    data = []
    for q in questions_qs:
        opts_qs = list(q.options.all())
        random.shuffle(opts_qs) 
        
        options_data = []
        for opt in opts_qs:
            options_data.append({
                'text': opt.text,
                'is_correct': opt.is_correct
            })
        
        data.append({
            'question': q.text,
            'options': options_data
        })
    
    return JsonResponse({'questions': data})