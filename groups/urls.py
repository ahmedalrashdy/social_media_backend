from django.urls import path
from .views import *

urlpatterns = [
     path('groups/', GroupListCreateAPIView.as_view(), name='group-list-create'),
    path('groups/<uuid:pk>/', GroupRetrieveUpdateDestroyAPIView.as_view(), name='group-detail'),
    # path('groups/<uuid:pk>/', GroupRetrieveUpdateDestroyAPIView.as_view(), name='group-detail'),

    # GroupPost
    # path('groups/posts/', GroupPostListAPIView.as_view(), name='group-post-list-create'),
    # path('groups/posts/<uuid:pk>/', GroupPostRetrieveUpdateDestroyAPIView.as_view(), name='group-post-detail'),

    path('posts/', GroupPostListAPIView.as_view(), name='post-list'),
    path('posts/<uuid:pk>/', GroupPostDetailAPIView.as_view(), name='post-detail'),
    path('posts/create/', GroupPostCreateAPIView.as_view(), name='post-create'),
    path('posts/<uuid:pk>/update/', GroupPostUpdateAPIView.as_view(), name='post-update'),
    path('posts/<uuid:pk>/delete/', GroupPostDeleteAPIView.as_view(), name='post-delete'),

    path('groups/interactions/posts/', GPostInteractionAPIView.as_view(), name='group-post-interaction'),
    path('groups/interactions/comments/', GCommentInteractionAPIView.as_view(), name='group-comment-interaction'),
    path('groups/interactions/replies/', GReplayInteractionAPIView.as_view(), name='group-replay-interaction'),
    path('groups/attachments/', GPostAttachmentAPIView.as_view(), name='group-post-attachment'),
]
