from django.urls import path
from links import views


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("recent/", views.RecentPostList.as_view(), name="recent-posts"),
    path("ask/", views.AskPostList.as_view(), name="ask-posts"),
    path("show/", views.ShowPostList.as_view(), name="show-posts"),
    path("create/", views.PostCreateView.as_view(), name="post-create"),
    path("p/<slug:post_slug>/flag/", views.PostFlagView.as_view(), name="post-flag"),
    path("p/<slug:slug>/", views.PostDetailView.as_view(), name="post-detail"),
]
