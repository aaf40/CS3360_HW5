# Schedule, sort, and process events of the simulation
class Event:
    def __init__(self, event_type, event_time, process):
        self.event_type = event_type 
        self.event_time = event_time
        self.process = process 

    def __lt__(self, other):
        return self.event_time < other.event_time
