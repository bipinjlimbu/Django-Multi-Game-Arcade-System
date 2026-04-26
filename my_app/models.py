from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=100, default='gamepad')
    color = models.CharField(max_length=20, default='blue')
    
    def __str__(self):
        return self.name

class QuizCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=50, default='help-circle')
    color = models.CharField(max_length=20, default='blue')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Leaderboard(models.Model):    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    quiz_category = models.ForeignKey(QuizCategory, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def formatted_score(self):
        if self.game.slug == 'memory-game':
            return f"{self.score / 100:.2f}s"
        return str(self.score)
    
    def __str__(self):
        return f"{self.user.username} - {self.game}: {self.score}"

class Question(models.Model):
    LEVEL_CHOICES = [
        (1, 'Easy'),
        (2, 'Medium'),
        (3, 'Hard'),
    ]
    category = models.ForeignKey(QuizCategory, on_delete=models.CASCADE, related_name='questions')
    level = models.IntegerField(choices=LEVEL_CHOICES, default=1)
    text = models.TextField()

    def __str__(self):
        return f"[{self.category.name} - Lvl {self.level}] {self.text[:50]}"

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'Correct' if self.is_correct else 'Wrong'})"