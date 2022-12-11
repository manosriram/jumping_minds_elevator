from django.shortcuts import render
from enum import Enum
import json

from django.core.cache import cache

from .elevator import Elevator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action

elevators = {}
class ElevatorSystem(APIView):

    def get(self, request):
        elevator_id = request.GET.get('id', None)
        show_all = request.GET.get('all', None)
        if show_all is not None and int(show_all) is 1:
            elevators_json = []
            for x in elevators.keys():
                elevators_json.append(vars(elevators[x]))

            return Response(elevators_json)

        elevator = elevators.get(int(elevator_id), None)
        return Response(vars(elevator))

    def post(self, request):
        elevators_count = request.data['elevators_count']

        if elevators_count:
            for i in range(0, elevators_count):
                elevators[i+1] = Elevator(i+1)

        return Response("intialized {} elevators".format(elevators_count))

    def put(self, request):
        door = request.data.get('door', None)
        if door == "closed":
            elevator_id = request.data['id']
            elevator = elevators.get(int(elevator_id))
            elevator.process_request_list()

            return Response("door status changed to closed")



        floor = request.data.get('floor', None)
        if floor is not None:
            mn = 1000
            for idx, e in enumerate(elevators.keys()):
                x = elevators[e]
                if abs(x.current_floor - floor) < mn:
                    mn = x.current_floor
                    mn_idx = x.id

            # find optimal elevator
            elevator = elevators.get(mn_idx, None)
            elevator.add_floor_to_request_list(floor)


            
        return Response({
            "id": elevator.id,
            "request_list": elevator.request_list
        })
