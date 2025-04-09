from email.policy import default
from random import choice
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings


from utils.choices import InteractionType
from utils.models import TimeStampedModel 


class Group(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_groups', on_delete=models.SET_NULL, null=True) 
    name = models.CharField(max_length=50)
    type = models.IntegerField(choices=[(0,"Private"),(1,"Public")],blank=True,default=0)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Membership',
        related_name='joined_groups'
    )

    def __str__(self):
        return self.name
    


class Membership(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="memberships")
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, default='member', choices=[('member', 'Member'), ('admin', 'Admin'), ('owner', 'Owner')])

    class Meta:
        unique_together = ('user', 'group')

    def __str__(self):
        return f"{self.user.name} in {self.group.name} ({self.role})"

class GroupPost(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='group_posts', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='posts', on_delete=models.CASCADE)
    text = models.TextField()
    

    def __str__(self):
        return f"Post by {self.author.name} in {self.group.name} ({self.id})"
    


class GroupPostComment(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='g_post_comments', on_delete=models.CASCADE)
    text = models.TextField()
    post=models.ForeignKey(GroupPost,on_delete=models.CASCADE,related_name='comments')


    def __str__(self):
        return f"Comment by {self.author.name} on {self.post}"
    


class GroupCommentReply(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='g_comment_replies', on_delete=models.CASCADE)
    comment = models.ForeignKey(GroupPostComment, related_name='replies', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"Reply by {self.author.name} to comment {self.comment.id}"
    
    
  
class GPostInteraction(TimeStampedModel):        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='g_post_interactions', on_delete=models.CASCADE)
    post=models.ForeignKey(GroupPost,on_delete=models.CASCADE,related_name='interactions')
    type = models.CharField(
        max_length=2,
        choices=InteractionType.choices,
        default=InteractionType.LIKE,
    )
    class Meta:
        unique_together = ('user','post')
       

    def __str__(self):
        return f"{self.user.username} {self.get_type_display()}"
    
    
class GCommentInteraction(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='g_comment_interactions', on_delete=models.CASCADE)
    comment=models.ForeignKey(GroupPostComment,on_delete=models.CASCADE,related_name='interactions')
    type = models.CharField(
        max_length=2,
        choices=InteractionType.choices,
        default=InteractionType.LIKE,
    )
    class Meta:
        unique_together = ('user','comment')
    def __str__(self):
        return f"{self.user.name} {self.get_type_display()}"
class GReplayInteraction(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='g_replay_interactions', on_delete=models.CASCADE)
    replay=models.ForeignKey(GroupCommentReply,on_delete=models.CASCADE,related_name='interactions')
    type = models.CharField(
        max_length=2,
        choices=InteractionType.choices,
        default=InteractionType.LIKE,
    )
    class Meta:
        unique_together = ('user','replay')

    def __str__(self):
        return f"{self.user.name} {self.get_type_display()}"
    
    


class GPostAttachment(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='attachments/group-post/%Y/%m/%d/')
    post=models.ForeignKey(GroupPost,on_delete=models.CASCADE,related_name='g_post_attachments')
    def __str__(self):
        return f"Attachment for {self.post}"