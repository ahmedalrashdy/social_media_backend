# posts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Posts
    path('posts/', views.PersonalPostListCreateAPIView.as_view(), name='post-list-create'),
    path('posts/<uuid:pk>/', views.PersonalPostDetailAPIView.as_view(), name='post-detail'),

    # Comments
    path('comments/create/', views.PersonalPostCommentCreateAPIView.as_view(), name='comment-create'),

    # Replies
    path('replies/create/', views.PersonalCommentReplyCreateAPIView.as_view(), name='reply-create'),

    # Interactions
    path('interactions/posts/', views.PPostInteractionCreateAPIView.as_view(), name='post-interaction'),
    path('interactions/comments/', views.PCommentInteractionCreateAPIView.as_view(), name='comment-interaction'),
    path('interactions/replies/', views.PReplayInteractionCreateAPIView.as_view(), name='reply-interaction'),

    # Attachments
    path('attachments/create/', views.PPostAttachmentCreateAPIView.as_view(), name='attachment-create'),
]