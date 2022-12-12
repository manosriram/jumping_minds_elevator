from enum import Enum

class ElevatorDoorStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"

class ElevatorCondition(str, Enum):
    WORKING = "working"
    UNDER_MAINTENANCE = "under_maintenance"

class Elevator:
    def __str__(self):
        pattern = '''
            id: {}
            current_floor: {}
            door: {}
            condition: {}
            request_list: {}
            direction: {}
        '''

        return pattern.format(self.id, self.current_floor, self.door, self.condition, self.request_list, self.direction)

    def __init__(self, id):
        self.id = id
        self.current_floor = 0
        self.door = ElevatorDoorStatus.OPEN
        self.condition = ElevatorCondition.WORKING
        self.request_list = []
        self.direction = 0

    # updates the direction of the elevator
    # 1 = up, -1 = down, 0 = elevator's request list empty
    def update_direction(self):
        request_list = self.request_list
        if len(request_list) > 0:
            if request_list[0] > self.current_floor:
                self.direction = 1
            elif request_list[0] < self.current_floor:
                self.direction = -1
            else:
                self.direction = 0
        else:
            self.direction = 0

    def open_door(self):
        print("opening door for elevator {} at floor {}".format(self.id, self.current_floor))
        self.door = ElevatorDoorStatus.OPEN
        self.update_direction()

    def close_door(self):
        print("closing door for elevator {} at floor {}".format(self.id, self.current_floor))
        self.door = ElevatorDoorStatus.CLOSED

    def add_floor_to_request_list(self, floor):
        self.request_list.append(int(floor))
        self.update_direction()

    # go to given floor from it's current floor
    def go_to_floor(self, floor):
        self.close_door()

        if floor < self.current_floor:
            self.direction = -1
            for x in range(self.current_floor, floor-1, -1):
                self.current_floor = x
                print("elevator {} via floor {}".format(self.id, self.current_floor))
        elif floor > self.current_floor:
            self.direction = 1
            for x in range(self.current_floor, floor+1):
                self.current_floor = x
                print("elevator {} via floor {}".format(self.id, self.current_floor))
        else:
            self.direction = 0

        self.open_door()
        self.update_direction()

    # process the next floor in request_list
    def process_request_list(self):
        if len(self.request_list) == 0:
            return

        next_floor = self.request_list.pop(0)
        self.go_to_floor(next_floor)

