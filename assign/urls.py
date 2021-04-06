from django.urls import path
from assign import views

urlpatterns = [
    path("", views.home, name="home"),
]
