from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("elevator/", views.initialize_elevators.as_view()),
    path("floor/", views.floor.as_view())
]
