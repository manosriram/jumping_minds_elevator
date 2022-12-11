from django.contrib import admin
from django.urls import path
from . import views

get_elevator_next_destination = views.ElevatorMeta.as_view({'get': 'get_elevator_next_destination'})
get_elevator_direction = views.ElevatorMeta.as_view({'get': 'get_elevator_direction'})

urlpatterns = [
    path("elevator/", views.ElevatorSystem.as_view(), name="elevator_create"),
    path("elevator/next/", get_elevator_next_destination, name="elevator_next"),
    path("elevator/direction/", get_elevator_direction, name="elevator_destination"),
]
