from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # path("add-question", views, name="add-question"),
    # path("view-question/<str:pk>", views, name="view-question"),
    # path("update-question/<str:pk>", views, name="update-question"),
    # path("delete-question/<str:pk>", views, name="delete-question"),
    # path("question/<str:pk>/add-answer", views, name="add-answer"),
    # path("question/<str:pk>/update-answer/<str:id>", views, name="update-answer"),
    # path("question/<str:pk>/delete-answer/<str:id>", views, name="delete-answer"),
    # path("question/<str:pk>/answer/<str:id>/like", views, name="like-answer"),
]
