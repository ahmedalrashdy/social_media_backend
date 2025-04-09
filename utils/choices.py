from django.db import models

class InteractionType(models.TextChoices):
        LIKE = 'LK', 'Like'
        DISLIKE = 'DL', 'Dislike'