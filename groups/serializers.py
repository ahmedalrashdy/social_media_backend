from rest_framework import serializers
from .models import (
    Group, Membership, GroupPost, GroupPostComment,
    GroupCommentReply, GPostInteraction, GCommentInteraction,
    GReplayInteraction, GPostAttachment
)

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields = ['id', 'creator']


class GroupPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupPost
        fields = '__all__'
        read_only_fields = ['id', 'author']


class GroupPostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupPostComment
        fields = '__all__'
        read_only_fields = ['id', 'author']


class GroupCommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupCommentReply
        fields = '__all__'
        read_only_fields = ['id', 'author']


class GPostInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPostInteraction
        fields = '__all__'
        read_only_fields = ['id', 'user']


class GCommentInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GCommentInteraction
        fields = '__all__'
        read_only_fields = ['id', 'user']


class GReplayInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GReplayInteraction
        fields = '__all__'
        read_only_fields = ['id', 'user']


class GPostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPostAttachment
        fields = '__all__'
        read_only_fields = ['id']
