# Elevator System

### APIs

1. Initialize elevator system
2. Request elevator for floor
3. Get elevator by Id
4. Get all elevators
5. Close elevator door (open by default)

### Flow

1. Initialize 'n' elevators
2. Request elevator for floor (assigns optimal elevator and updates it's request_list)
3. Close elevator's door

One assumption I've made is elevator doesn't move until we close the door. This allows us to use the APIs and see the live states. So, we need to call the close elevator API (`/elevator/door`) inorder to update the `request_list` and the `current_floor` of the elevator.

4. Get all elevators or by id to see current state of the elevator.

### Elevator States

1. condition -> `working` or `under_maintenance`, elevator isn't considered if it's condition is `under_maintenance`
2. direction -> `1 = up`, `-1 = down`, `0 = request_list is empty`
3. door -> `open`, `closed`
4. current_floor -> the floor where elevator is at
5. request_list -> list of requests

`elevator` dict has `n` elevator instances with keys starting from 1 to n

### Assigning elevator

Elevator is assigned by calculating the distance from the requested floor to all elevators and picking the one with minimum distance.

### Setup

Run `docker-compose up` to start the server at port 8000.

### API definitions

1. Initialize elevator system

`elevator/init/`

```
{
    "elevators_count": 5
}
```

2. Request elevator for floor

`elevator/request/`

```
{
    "floor": 4
}
```

3. Get Elevator by Id

`elevator/?id=1`

4. Get all Elevators

`elevator/`

5. Close elevator door

`elevator/door/`

```
{
    "id": 1,
    "door": "closed"
}
```

6. Get elevator condition

`elevator/condition/`

```
{
    "id": 1,
    "condition": "under_maintenance"
}
```

7. Get next floor for an elevator

`elevator/next/?id=1`

8. Get direction of elevator

`elevator/direction/?id=1`
