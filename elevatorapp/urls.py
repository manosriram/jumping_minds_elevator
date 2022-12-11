from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("elevator/", views.ElevatorSystem.as_view()),
    #  path("elevator/door", views.El
    #  path("floor/", views.Floor.as_view())
]
