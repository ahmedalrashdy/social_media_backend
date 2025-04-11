

from . import views


from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ( PersonalPostInteractView ,
                    PersonalPostCreateView, PersonalPostListView,
                    PersonalPostRetrieveView,
                    PersonalPostDeleteView,PersonalPostUpdateView)
urlpatterns = [
    path("",PersonalPostListView.as_view(),name="personal-posts-list"),
    path("posts/create/",PersonalPostCreateView.as_view(),name="personal-posts-create"),
    path("posts/<str:pk>",PersonalPostRetrieveView.as_view(),name="personal-posts-retrieve"),
    path("posts/<str:pk>/update/",PersonalPostUpdateView.as_view(),name="personal-posts-update"),
    path("posts/<str:pk>/delete/",PersonalPostDeleteView.as_view(),name="personal-posts-delete"),
    path('posts/<uuid:post_id>/interact/', PersonalPostInteractView.as_view(), name='personal-posts-interact'),

    # Comments
    path('comments/create/', views.PersonalPostCommentCreateAPIView.as_view(), name='comment-create'),

    # Replies
    path('replies/create/', views.PersonalCommentReplyCreateAPIView.as_view(), name='reply-create'),

    # Interactions
    path('interactions/comments/', views.PCommentInteractionCreateAPIView.as_view(), name='comment-interaction'),
    path('interactions/replies/', views.PReplayInteractionCreateAPIView.as_view(), name='reply-interaction'),

    # Attachments
    path('attachments/create/', views.PPostAttachmentCreateAPIView.as_view(), name='attachment-create'),
    
]
