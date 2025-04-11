# posts/serializers.py

from rest_framework import serializers
from .models import (
    PersonalPost, PersonalPostComment, PersonalCommentReply,
    PPostInteraction, PCommentInteraction, PReplayInteraction,
    PPostAttachment
)

class PersonalPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)

    class Meta:
        model = PersonalPost
        fields = '__all__'
        read_only_fields = ['id', 'author']

class PersonalPostCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)

    class Meta:
        model = PersonalPostComment
        fields = '__all__'
        read_only_fields = ['id', 'author']

class PersonalCommentReplySerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)

    class Meta:
        model = PersonalCommentReply
        fields = '__all__'
        read_only_fields = ['id', 'author']

class PPostInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PPostInteraction
        fields = '__all__'
        read_only_fields = ['id', 'user']

class PCommentInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PCommentInteraction
        fields = '__all__'
        read_only_fields = ['id', 'user']

class PReplayInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PReplayInteraction
        fields = '__all__'
        read_only_fields = ['id', 'user']

class PPostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PPostAttachment
        fields = '__all__'
        read_only_fields = ['id']
