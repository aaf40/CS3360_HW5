# Schedule, sort, and process events of the simulation
class Event:
    def __init__(self, event_type, event_time, process, cpu_index=None):
        self.event_type = event_type
        self.event_time = event_time
        self.process = process
        self.cpu_index = cpu_index

    def __lt__(self, other):
        return self.event_time < other.event_time

