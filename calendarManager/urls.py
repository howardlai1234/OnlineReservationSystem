from django.urls import path
from calendarManager import views

urlpatterns = [
    path("", views.home, name="home"),
    path("confirm", views.confirm, name="confirm_entry"),
    path("remove", views.remove, name="remove_slot"),
    path("minimumslot", views.setMinSlot, name='setminslot'),
]
