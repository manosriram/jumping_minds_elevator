from django.shortcuts import render
from enum import Enum
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response

import pickle
import json

from django_redis import get_redis_connection
con = get_redis_connection("default")

class ElevatorDoor(str, Enum):
    OPEN = "open"
    CLOSED = "closed"

class ElevatorCondition(str, Enum):
    WORKING = "working"
    UNDER_MAINTENANCE = "under_maintenance"

class ElevatorStatus(str, Enum):
    AVAILABLE = "available"
    BUSY = "busy"


def pickle_elevator(raw_elevator):
    return pickle.dumps(raw_elevator)

def depickle_elevator(pickled_elevator):
    return pickle.loads(pickled_elevator)

class ElevatorItem:
    def __init__(self, id, current_floor):
        self.elevator_id = id
        self.current_floor = current_floor
        self.status = ElevatorStatus.AVAILABLE
        self.condition = ElevatorCondition.WORKING
        self.door = ElevatorDoor.CLOSED

def update_elevator_condition(raw_elevator, elevator_condition):
    elevator = depickle_elevator(raw_elevator)
    elevator.condition = elevator_condition
    con.lset("elevator", elevator.elevator_id, pickle_elevator(elevator))

def update_elevator_floor(raw_elevator, floor):
    elevator = pickle_elevator(raw_elevator)
    elevator.current_floor = floor
    con.lset("elevator", elevator.elevator_id, depickle_elevator(elevator))

class Elevator(APIView):

    def get(self, request):
        lst = con.lrange("elevator", 0, -1)
        #  print(lst)
        elevators = []
        for x in lst:
            p = pickle.loads(x)
            elevators.append({
                "id": p.elevator_id,
                "current_floor": p.current_floor,
                "condition": json.dumps(p.condition).replace('\"',""),
                "status": json.dumps(p.status).replace('\"',""),
                "door": json.dumps(p.door).replace('\"',""),
            })

        return Response(elevators)

    def post(self, request):
        count = request.data['count']
        con.delete("elevator")

        for i in range(count):
            new_elevator = ElevatorItem(i, 0)
            new_elevator_serialized = pickle.dumps(new_elevator)
            con.rpush("elevator", new_elevator_serialized)

        print(request.data)

        return Response("done")
    
    def put(self, request):
        data = request.data

        elevator_id = data['elevator_id']
        e = con.lindex("elevator", int(elevator_id))

        elevator_condition = data['elevator_condition']

        if elevator_condition:
            update_elevator_condition(e, elevator_condition)

        return Response("done condition")


class Floor(APIView):

    def post(self, request):
        floor = request.data['floor']
        r = con.lrange("elevator", 0, -1)

        mn = 10000
        o = None
        for idx, xx in enumerate(r):
            x = pickle.loads(xx)
            if int(x.current_floor) == int(floor) or x.condition != ElevatorCondition.WORKING:
                continue

            if abs(int(x.current_floor) - int(floor)) < mn:
                mn_idx = idx
                o = x
                mn = abs(int(x.current_floor) - int(floor))

            print("mn_idx = ", mn_idx)
            print("mn = ", mn)

        if o is not None:
            o.current_floor = floor
            con.lset("elevator", mn_idx, pickle.dumps(o))

        return Response("done floor")

        """
            1. loop through the elevators, find minimum distance between floor & elevator;
            2. pick that elevator, change its value to {floor}
        """


def hit_view(request):
    pass
