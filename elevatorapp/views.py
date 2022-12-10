from django.shortcuts import render
from enum import Enum
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response

from django_redis import get_redis_connection
con = get_redis_connection("default")


elevator = []

class ElevatorStatus(Enum):
    AVAILABLE = 1
    BUSY = 2

def move_elevator(elevator_id, src_floor, dest_floor):
    pass

def update_elevator_status(elevator_id, status):
    pass



class initialize_elevators(APIView):
    #  no_of_elevators = request.data
    def get(self, request):
        lst = con.lrange("elevator", 0, -1)
        return Response(lst)

    def post(self, request):
        count = request.data['count']
        con.delete("elevator")

        for i in range(count):
            con.lpush("elevator", 0)

        print(request.data)

        return Response("done")

class floor(APIView):

    def post(self, request):
        floor = request.data['floor']
        r = con.lrange("elevator", 0, -1)
        #  print("r = ", r)
        mn = 10000
        #  mn_idx = 0
        for idx, x in enumerate(r):
            if int(x) == int(floor):
                continue
            #  if x == lget("elevator", idx):
                #  continue

            if abs(int(x) - int(floor)) < mn:
                mn_idx = idx
                mn = abs(int(x) - int(floor))

            print("mn_idx = ", mn_idx)
            print("mn = ", mn)

        con.lset("elevator", mn_idx, floor)
        return Response("done floor")

        """
            1. loop through the elevators, find minimum distance between floor & elevator;
            2. pick that elevator, change its value to {floor}
        """


def hit_view(request):
    pass
