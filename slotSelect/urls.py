from django.urls import path
from slotSelect import views

urlpatterns = [
    path("", views.home, name="home"),
]
