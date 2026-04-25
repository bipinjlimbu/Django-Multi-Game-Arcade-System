from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=100, default='gamepad')
    color = models.CharField(max_length=20, default='blue')
    
    def __str__(self):
        return self.name
    
class Leaderboard(models.Model):    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def formatted_score(self):
        if self.game.slug == 'memory-game':
            return f"{self.score / 100:.2f}s"
        return str(self.score)
    
    def __str__(self):
        return f"{self.user.username} - {self.game}: {self.score}"