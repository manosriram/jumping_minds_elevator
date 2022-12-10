from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("elevator/", views.Elevator.as_view()),
    path("floor/", views.Floor.as_view())
]
