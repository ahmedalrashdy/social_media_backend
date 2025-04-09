
import uuid
from django.db import models

from django.conf import settings

from utils.choices import InteractionType
from utils.models import TimeStampedModel 

class Channel(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_channels', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    subscribers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='ChannelSubscription',
        related_name='subscribed_channels'
    )

    def __str__(self):
        return self.name

class ChannelSubscription(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="subscriptions")
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, default='subscriber', choices=[('subscriber', 'Subscriber'), ('admin', 'admin'), ('owner', 'owner')]) 

    class Meta:
        unique_together = ('user', 'channel')

    def __str__(self):
        return f"{self.user.name} subscribed to {self.channel.name} ({self.role})"


class ChannelPost(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='channel_posts', on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, related_name='posts', on_delete=models.CASCADE)
    text = models.TextField()
    def __str__(self):
        return f"Post by {self.author.name} in {self.channel.name} ({self.id})"





class ChannelPostComment(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='c_post_comments', on_delete=models.CASCADE)
    text = models.TextField()
    post=models.ForeignKey(ChannelPost,on_delete=models.CASCADE,related_name='comments')


    def __str__(self):
        return f"Comment by {self.author.name} on {self.post}"
    
    
    




class ChannelCommentReply(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='c_comment_replies', on_delete=models.CASCADE)
    comment = models.ForeignKey(ChannelPostComment, related_name='replies', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"Reply by {self.author.name} to comment {self.comment.id}"
    
    
    
    
class CPostInteraction(TimeStampedModel):        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='c_post_interactions', on_delete=models.CASCADE)
    post=models.ForeignKey(ChannelPost,on_delete=models.CASCADE,related_name='interactions')
    type = models.CharField(
        max_length=2,
        choices=InteractionType.choices,
        default=InteractionType.LIKE,
    )
    class Meta:
        unique_together = ('user','post')
       

    def __str__(self):
        return f"{self.user.name} {self.get_type_display()}"
    
    
class CCommentInteraction(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='c_comment_interactions', on_delete=models.CASCADE)
    comment=models.ForeignKey(ChannelPostComment,on_delete=models.CASCADE,related_name='interactions')
    type = models.CharField(
        max_length=2,
        choices=InteractionType.choices,
        default=InteractionType.LIKE,
    )
    class Meta:
        unique_together = ('user','comment')
    def __str__(self):
        return f"{self.user.name} {self.get_type_display()}"
class CReplayInteraction(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='c_replay_interactions', on_delete=models.CASCADE)
    replay=models.ForeignKey(ChannelCommentReply,on_delete=models.CASCADE,related_name='interactions')
    type = models.CharField(
        max_length=2,
        choices=InteractionType.choices,
        default=InteractionType.LIKE,
    )
    class Meta:
        unique_together = ('user','replay')

    def __str__(self):
        return f"{self.user.name} {self.get_type_display()}"
    
    


class CPostAttachment(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='attachments/channel-post/%Y/%m/%d/')
    post=models.ForeignKey(ChannelPost,on_delete=models.CASCADE,related_name='c_post_attachments')
    def __str__(self):
        return f"Attachment for {self.post}"