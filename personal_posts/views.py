# posts/views.py

from rest_framework import generics, permissions
from .models import *
from .serializers import *

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or obj.author == request.user

# --- Personal Posts ---
class PersonalPostListCreateAPIView(generics.ListCreateAPIView):
    queryset = PersonalPost.objects.all()
    serializer_class = PersonalPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PersonalPostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PersonalPost.objects.all()
    serializer_class = PersonalPostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


# --- Comments ---
class PersonalPostCommentCreateAPIView(generics.CreateAPIView):
    queryset = PersonalPostComment.objects.all()
    serializer_class = PersonalPostCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# --- Replies ---
class PersonalCommentReplyCreateAPIView(generics.CreateAPIView):
    queryset = PersonalCommentReply.objects.all()
    serializer_class = PersonalCommentReplySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# --- Interactions ---
class PPostInteractionCreateAPIView(generics.CreateAPIView):
    queryset = PPostInteraction.objects.all()
    serializer_class = PPostInteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PCommentInteractionCreateAPIView(generics.CreateAPIView):
    queryset = PCommentInteraction.objects.all()
    serializer_class = PCommentInteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PReplayInteractionCreateAPIView(generics.CreateAPIView):
    queryset = PReplayInteraction.objects.all()
    serializer_class = PReplayInteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# --- Attachments ---
class PPostAttachmentCreateAPIView(generics.CreateAPIView):
    queryset = PPostAttachment.objects.all()
    serializer_class = PPostAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]
