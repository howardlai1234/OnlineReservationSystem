from django.urls import path
from login import views

urlpatterns = [
    path("", views.home, name="home"),
    path("test", views.connction_test, name="sql_test"),
    path("PasswordRecover", views.pass_recov, name="PasswordRecover"),
    path("logout", views.logout, name="logout")
]
