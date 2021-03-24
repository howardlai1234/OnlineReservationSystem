from django.urls import path
from message import views

urlpatterns = [
    path("", views.home, name="home"),
    path("view", views.view, name="view_message"),
    path("create", views.create_new, name="new_message")
]
