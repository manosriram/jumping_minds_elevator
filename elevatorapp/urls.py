from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("elevator/", views.ElevatorSystem.as_view(), name="elevator_create"),
]
