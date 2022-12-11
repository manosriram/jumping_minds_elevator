from django.shortcuts import render
from enum import Enum
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
import json

elevators = {}

class Elevator:
    def __str__(self):

        pattern = '''
            id: {}
            current_floor: {}
            door: {}
            status: {}
            request_list: {}
            direction: {}
        '''

        return pattern.format(self.id, self.current_floor, self.door, self.status, self.request_list, self.direction)

    def __init__(self, id):
        self.id = id
        self.current_floor = 0
        self.door = "closed"
        self.status = "working"
        self.request_list = []
        self.direction = 0

    def open_door(self):
        print("opening door for elevator {} at floor {}".format(self.id, self.current_floor))
        self.door = "open"

        request_list = self.request_list
        if len(request_list) > 0:
            print("in req")
            if request_list[0] > self.current_floor:
                self.direction = 1
            elif request_list[0] < self.current_floor:
                self.direction = -1
            else:
                self.direction = 0
        else:
            self.direction = 0


    def close_door(self):
        print("closing door for elevator {} at floor {}".format(self.id, self.current_floor))
        self.door = "closed"

    def add_floor_to_request_list(self, floor):
        self.request_list.append(int(floor))

    def go_to_floor(self, floor):
        self.close_door()

        # go from self.current_floor to floor
        if floor < self.current_floor:
            self.direction = -1
            for x in range(self.current_floor-1, floor, -1):
                self.current_floor = x
                print("elevator {} via floor {}".format(self.id, self.current_floor))
        elif floor > self.current_floor:
            self.direction = 1
            for x in range(self.current_floor+1, floor):
                self.current_floor = x
                print("elevator {} via floor {}".format(self.id, self.current_floor))
        else:
            self.direction = 0

        self.current_floor += 1
        self.open_door()

    def process_request_list(self):
        next_floor = self.request_list.pop(0)
        self.go_to_floor(next_floor)





class ElevatorSystem(APIView):

    pass
