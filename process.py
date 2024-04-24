# Defines the properties and behavior of a process in the simulation
import itertools

class Process:
    _pid_generator = itertools.count(1)

    def __init__(self, arrival_time, service_time):
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.pid = next(self._pid_generator)
        self.wait_time = 0

    def update_wait_time(self, current_time):
        self.wait_time += current_time - self.arrival_time


