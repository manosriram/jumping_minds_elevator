from django.contrib import admin
from django.urls import path
from . import views

get_elevator_next_destination = views.ElevatorMeta.as_view({'get': 'get_elevator_next_destination'})
get_elevator_direction = views.ElevatorMeta.as_view({'get': 'get_elevator_direction'})

get_elevator = views.ElevatorSystem.as_view({ 'get': 'get_elevator' })
initialize_elevators = views.ElevatorSystem.as_view({ 'post': 'initialize_elevators' })
update_door_status = views.ElevatorSystem.as_view({ 'put': 'update_door_status' })
request_elevator = views.ElevatorSystem.as_view({ 'put': 'request_elevator' })
update_elevator_condition = views.ElevatorSystem.as_view({ 'put': 'update_condition' })

urlpatterns = [
    path("elevator/", get_elevator, name="elevator_create"),
    path("elevator/init/", initialize_elevators, name="elevator_init"),
    path("elevator/door/", update_door_status, name="elevator_door_update"),
    path("elevator/condition/", update_elevator_condition, name="elevator_door_update"),
    path("elevator/request/", request_elevator, name="elevator_door_update"),


    path("elevator/next/", get_elevator_next_destination, name="elevator_next"),
    path("elevator/direction/", get_elevator_direction, name="elevator_destination"),
]
