from django.shortcuts import render
import json

from django.core.cache import cache
import pickle

from .elevator import Elevator, ElevatorCondition, ElevatorDoorStatus

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action

elevators = {}

class ElevatorMeta(viewsets.ViewSet):
    @action(methods=['get'], detail=False)    
    def get_elevator_next_destination(self, request):
        elevator_id = request.GET.get('id', None)
        elevator = elevators.get(int(elevator_id))
        
        if len(elevator.request_list) == 0:
            return Response({ "message": "request list empty" })
        else:
            return Response({ "floor": elevator.request_list[0] })

    @action(methods=['get'], detail=False)    
    def get_elevator_direction(self, request):
        elevator_id = request.GET.get('id', None)
        elevator = elevators.get(int(elevator_id))

        if len(elevator.request_list) == 0:
            return Response({ "message": "request list empty" })
        else:
            direction = "up" if elevator.direction == 1 else "down"
            return Response({ "direction": direction })


class ElevatorSystem(APIView):

    def get(self, request):
        elevatorx = pickle.loads(cache.get("elevators"))

        elevator_id = request.GET.get('id', None)
        if elevator_id is not None:
            elevator = elevators.get(int(elevator_id), None)
            return Response(vars(elevator))

        elevators_json = []
        for x in elevators.keys():
            elevators_json.append(vars(elevatorx[x]))

        return Response(elevators_json)

    def post(self, request):
        elevators_count = request.data['elevators_count']

        if elevators_count:
            for i in range(0, elevators_count):
                elevators[i+1] = Elevator(i+1)

        cache.set("elevators", pickle.dumps(elevators))

        return Response("intialized {} elevators".format(elevators_count))

    def put(self, request):
        door = request.data.get('door', None)
        if door == ElevatorDoorStatus.CLOSED:
            elevator_id = request.data['id']
            elevator = elevators.get(int(elevator_id))
            elevator.process_request_list()

            cache.set("elevators", pickle.dumps(elevators))

            return Response("door status changed to closed")


        floor = request.data.get('floor', None)
        if floor is not None:
            min_diff = 1000
            elevator_index = len(elevators)

            for idx, e in enumerate(elevators.keys()):
                x = elevators[e]
                if abs(x.current_floor - floor) < min_diff:
                    min_diff = abs(x.current_floor - floor)
                    elevator_index = e
                    elevator = x

            elevator = elevators.get(elevator_index, None)
            elevator.add_floor_to_request_list(floor)

            cache.set("elevators", pickle.dumps(elevators))
        
        condition = request.data.get('condition', None)
        if condition is None:
            return Response({
                "id": elevator.id,
                "request_list": elevator.request_list
            })

        if condition not in [ElevatorCondition.WORKING, ElevatorCondition.UNDER_MAINTENANCE]:
            return Response({ "message": "condition should be either working or under_maintenance" })

        elevator_id = request.data['id']
        elevator = elevators.get(int(elevator_id))
        elevator.condition = condition

        cache.set("elevators", pickle.dumps(elevators))

        return Response({
            "id": elevator.id,
            "condition": elevator.condition
        })


