from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path("add-question", views.add_question, name="add-question"),
    path("view-question/<str:pk>", views.view_question, name="view-question"),
    path("update-question/<str:pk>", views.update_question, name="update-question"),
    path("delete-question/<str:pk>", views.delete_question, name="delete-question"),
    path("question/<str:pk>/add-answer", views.add_answer, name="add-answer"),
    path("update-answer/<str:ans_id>", views.update_answer, name="update-answer"),
    path("answer/<str:answer_id>/like", views.like_answer, name="like-answer"),
]
