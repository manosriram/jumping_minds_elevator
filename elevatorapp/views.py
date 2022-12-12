from django.shortcuts import render
import json

from django.core.cache import cache
import pickle

from .elevator import Elevator, ElevatorCondition, ElevatorDoorStatus

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status

elevators = {}

class ElevatorMeta(viewsets.ViewSet):

    @action(methods=['get'], detail=False)    
    def get_elevator_next_destination(self, request):
        elevator_id = request.GET.get('id', None)
        elevator = elevators.get(int(elevator_id))

        if not elevator:
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "message": "elevator not found" })
        
        if len(elevator.request_list) == 0:
            return Response(status=status.HTTP_200_OK, data = { "message": "request list empty" })
        else:
            return Response(status=status.HTTP_200_OK, data = { "floor": elevator.request_list[0] })

    @action(methods=['get'], detail=False)    
    def get_elevator_direction(self, request):
        elevator_id = request.GET.get('id', None)
        elevator = elevators.get(int(elevator_id))

        if not elevator:
            return Response(status=status.HTTP_404_NOT_FOUND, data = { "message": "elevator not found" })

        if len(elevator.request_list) == 0:
            return Response({ "message": "request list empty" })
        else:
            direction = "up" if elevator.direction == 1 else "down"
            return Response(status=status.HTTP_200_OK, data = { "direction": direction })


class ElevatorSystem(viewsets.ViewSet):

    @action(methods=['get'], detail=False)    
    def get_elevator(self, request):
        elevatorx = pickle.loads(cache.get("elevators"))

        elevator_id = request.GET.get('id', None)
        if elevator_id is not None:
            elevator = elevators.get(int(elevator_id), None)
            if not elevator:
                return Response(status=status.HTTP_404_NOT_FOUND, data = { "message": "elevator not found" })
            return Response(vars(elevator))

        elevators_json = []
        for x in elevators.keys():
            elevators_json.append(vars(elevatorx[x]))

        return Response(elevators_json)

    @action(methods=['post'], detail=False)    
    def initialize_elevators(self, request):
        elevators_count = request.data['elevators_count']

        if elevators_count:
            for i in range(0, elevators_count):
                elevators[i+1] = Elevator(i+1)

        cache.set("elevators", pickle.dumps(elevators))

        return Response(status=status.HTTP_200_OK, data = {"message": "intialized {} elevators".format(elevators_count)} )


    @action(methods=['put'], detail=False)    
    def update_door_status(self, request):
        door = request.data.get('door', None)
        if door == ElevatorDoorStatus.CLOSED:
            elevator_id = request.data['id']
            elevator = elevators.get(int(elevator_id))
            if not elevator:
                return Response(status=status.HTTP_404_NOT_FOUND, data = { "message": "elevator not found" })

            elevator.process_request_list()

            cache.set("elevators", pickle.dumps(elevators))

            return Response(status=status.HTTP_200_OK, data = {"message": "door status changed to closed" })

    @action(methods=['put'], detail=False)    
    def request_elevator(self, request):
        floor = request.data.get('floor', None)
        min_diff = 1000
        elevator_index = len(elevators)

        for idx, e in enumerate(elevators.keys()):
            x = elevators[e]
            if x.condition != ElevatorCondition.WORKING:
                continue
            if abs(x.current_floor - floor) < min_diff:
                min_diff = abs(x.current_floor - floor)
                elevator_index = e
                elevator = x

        elevator = elevators.get(elevator_index, None)
        if not elevator:
            return Response(status=status.HTTP_200_OK, data={
                "message": "all elevators under_maintenance"
            })

        if not elevator.check_valid_floor(floor):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "not a valid floor"})

        elevator.add_floor_to_request_list(floor)

        cache.set("elevators", pickle.dumps(elevators))
        return Response(status=status.HTTP_200_OK, data={
            "id": elevator.id,
            "condition": elevator.condition
        })

    @action(methods=['put'], detail=False)    
    def update_condition(self, request):
        condition = request.data.get('condition', None)
        if condition is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                "message": "condition empty"
            })


        if condition not in [ElevatorCondition.WORKING, ElevatorCondition.UNDER_MAINTENANCE]:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={ "message": "condition should be either working or under_maintenance" })

        elevator_id = request.data['id']
        elevator = elevators.get(int(elevator_id))
        elevator.condition = condition

        cache.set("elevators", pickle.dumps(elevators))

        return Response(status=status.HTTP_200_OK, data={
            "id": elevator.id,
            "condition": elevator.condition
        })
