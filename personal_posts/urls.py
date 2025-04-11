
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ( PersonalPostInteractView ,
                    PersonalPostCreateView, PersonalPostListView,
                    PersonalPostRetrieveView,
                    PersonalPostDeleteView,PersonalPostUpdateView)
urlpatterns = [
    path("",PersonalPostListView.as_view(),name="personal-posts-list"),
    path("create/",PersonalPostCreateView.as_view(),name="personal-posts-create"),
    path("<str:pk>",PersonalPostRetrieveView.as_view(),name="personal-posts-retrieve"),
    path("<str:pk>/update/",PersonalPostUpdateView.as_view(),name="personal-posts-update"),
    path("<str:pk>/delete/",PersonalPostDeleteView.as_view(),name="personal-posts-delete"),
    path('<uuid:post_id>/interact/', PersonalPostInteractView.as_view(), name='personal-posts-interact'),
]
