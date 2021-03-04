from django.urls import path
from calendarManager import views

urlpatterns = [
    path("", views.home, name="home"),

]