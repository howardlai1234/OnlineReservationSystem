from django.urls import path
from meeting import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create_new", views.create_new, name="new_meeting" )
]
