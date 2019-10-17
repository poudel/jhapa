from django.urls import path
from links import views


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("recent/", views.RecentPostList.as_view(), name="recent-posts"),
    path("create/", views.PostCreateView.as_view(), name="post-create"),
    path(
        "detail/<slug:slug>/",
        views.PostDetailView.as_view(),
        name="post-detail",
    ),
]
