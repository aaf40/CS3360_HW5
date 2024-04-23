import random
import math
import queue
from process import Process
from event import Event

class Simulator:
    def __init__(self, lambda_rate, average_service_time):
        self.lambda_rate = lambda_rate
        self.average_service_time = average_service_time
        self.processes_completed = 0
        self.clock = 0
        self.CPU_busy = False
        self.event_queue = queue.PriorityQueue()
        self.ready_queue = queue.Queue()
        self.total_waiting_time = 0
        self.total_service_time = 0
        self.total_turnaround_time = 0
        self.ready_queue_length_samples = []
        self.total_processes_arrived = 0

    def run(self):

        initial_process = self.generate_process(0)
        self.schedule_event("ARRIVAL", initial_process.arrival_time, initial_process)

        while not self.end_condition():
            if not self.event_queue.empty():
                event = self.event_queue.get()
                self.clock = event.event_time

                if event.event_type == "ARRIVAL":
                    self.handle_arrival(event)
                elif event.event_type == "DEPARTURE":
                    self.handle_departure(event)
        if self.end_condition():
            self.report_metrics()

    def handle_arrival(self, event):
        if not self.CPU_busy:
            self.CPU_busy = True
            departure_time = self.clock + event.process.service_time
            self.schedule_event("DEPARTURE", departure_time, event.process)
        else:
            self.ready_queue.put(event.process)
        
        next_process = self.generate_process(self.clock)
        self.schedule_event("ARRIVAL", next_process.arrival_time, next_process)
        self.total_processes_arrived += 1

    def handle_departure(self, event):
        if self.ready_queue.empty():
            self.CPU_busy = False
        else:
            next_process = self.ready_queue.get()
            departure_time = self.clock + next_process.service_time
            self.schedule_event("DEPARTURE", departure_time, next_process)
        self.processes_completed += 1
        self.total_service_time += event.process.service_time
        waiting_time = self.clock - event.process.arrival_time - event.process.service_time
        self.total_waiting_time += max(0, waiting_time)
        turnaround_time = self.clock - event.process.arrival_time
        self.total_turnaround_time += turnaround_time
        self.ready_queue_length_samples.append(self.ready_queue.qsize())

    def generate_process(self, last_arrival_time):
        inter_arrival_time = self.generate_exponential(1.0 / self.lambda_rate)
        service_time = self.generate_exponential(self.average_service_time)
        arrival_time = last_arrival_time + inter_arrival_time
        new_process = Process(arrival_time, service_time)
        return new_process

    def generate_service_time(self):
        return self.generate_exponential(self.average_service_time)

    def generate_exponential(self, mean):
        return -mean * math.log(1 - random.random())
    
    def end_condition(self):
        return self.processes_completed >= 10000

    def schedule_event(self, event_type, event_time, process):
        new_event = Event(event_type, event_time, process)
        self.event_queue.put(new_event)

    def report_metrics(self):
        average_waiting_time = self.total_waiting_time / self.processes_completed
        average_turnaround_time = self.total_turnaround_time / self.processes_completed
        total_throughput = self.processes_completed / self.clock
        CPU_utilization = self.total_service_time / self.clock
        average_ready_queue_length = sum(self.ready_queue_length_samples) / len(self.ready_queue_length_samples) if self.ready_queue_length_samples else 0

        #print(f"Average Waiting Time: {average_waiting_time}")
        print(f"Average Turnaround Time: {average_turnaround_time}")
        print(f"Total Throughput: {total_throughput}")
        print(f"CPU Utilization: {CPU_utilization * 100}%")
        print(f"Average Number of Processes in Ready Queue: {average_ready_queue_length}")
