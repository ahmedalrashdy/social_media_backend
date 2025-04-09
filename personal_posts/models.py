from django.db import models
from email.policy import default
from random import choice
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from accounts.models import User
from utils.models import TimeStampedModel 
# Create your models here.
class PersonalPost(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='personal_posts', on_delete=models.CASCADE)
    text = models.TextField()
    def __str__(self):
        return f"Post by {self.author.name} ({self.id})"



class PersonalPostComment(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='p_post_comments', on_delete=models.CASCADE)
    text = models.TextField()
    post=models.ForeignKey(PersonalPost,on_delete=models.CASCADE,related_name='comments')
    
    def __str__(self):
        return f"Comment by {self.author.name} on {self.post}"
    
class PersonalCommentReply(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='p_comment_replies', on_delete=models.CASCADE)
    comment = models.ForeignKey(PersonalPostComment, related_name='replies', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"Reply by {self.author.name} to comment {self.comment.id}"
    
class PPostInteraction(TimeStampedModel):

    class InteractionType(models.TextChoices):
        LIKE = 'LK', 'Like'
        DISLIKE = 'DL', 'Dislike'
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='p_post_interactions', on_delete=models.CASCADE)
    post=models.ForeignKey(PersonalPost,on_delete=models.CASCADE,related_name='interactions')
    type = models.CharField(
        max_length=2,
        choices=InteractionType.choices,
        default=InteractionType.LIKE,
    )
    class Meta:
        unique_together = ('user','post')
      

    def __str__(self):
        return f"{self.user.name} {self.get_type_display()}"
    
    
class PCommentInteraction(TimeStampedModel):

    class InteractionType(models.TextChoices):
        LIKE = 'LK', 'Like'
        DISLIKE = 'DL', 'Dislike'
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='p_comment_interactions', on_delete=models.CASCADE)
    comment=models.ForeignKey(PersonalPostComment,on_delete=models.CASCADE,related_name='interactions')
    type = models.CharField(
        max_length=2,
        choices=InteractionType.choices,
        default=InteractionType.LIKE,
    )
    class Meta:
        unique_together = ('user','comment')
       

    def __str__(self):
        return f"{self.user.name} {self.get_type_display()}"
class PReplayInteraction(TimeStampedModel):

    class InteractionType(models.TextChoices):
        LIKE = 'LK', 'Like'
        DISLIKE = 'DL', 'Dislike'
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='p_replay_interactions', on_delete=models.CASCADE)
    replay=models.ForeignKey(PersonalCommentReply,on_delete=models.CASCADE,related_name='interactions')
    type = models.CharField(
        max_length=2,
        choices=InteractionType.choices,
        default=InteractionType.LIKE,
    )
    class Meta:
        unique_together = ('user','replay')

    def __str__(self):
        return f"{self.user.name} {self.get_type_display()}"
    
    


class PPostAttachment(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='attachments/personal-post/%Y/%m/%d/')
    post=models.ForeignKey(PersonalPost,on_delete=models.CASCADE,related_name='attachments')
    
    def __str__(self):
        return f"Attachment for {self.post}"