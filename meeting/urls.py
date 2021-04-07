from django.urls import path
from meeting import views

urlpatterns = [
    path("", views.home, name="home"),
    path("view", views.view, name="view"),
    path("Manage", views.manage, name="manage"),
]
