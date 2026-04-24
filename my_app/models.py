from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Leaderboard(models.Model):
    class choices(models.TextChoices):
        GUESS_GAME = 'Guess Game'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    game = models.CharField(max_length=50, choices=choices.choices)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.game}: {self.score}"