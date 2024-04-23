import random
import math
import queue
from process import Process
from event import Event
from cpu import CPU

class MultiCPUSimulator:
    def __init__(self, lambda_rate, average_service_time, num_cpus, scenario):
        if num_cpus <= 0:
            raise ValueError("Number of CPUs must be greater than zero.")
        if scenario not in [1, 2]:
            raise ValueError("Scenario must be either 1 or 2.")

        self.lambda_rate = lambda_rate
        self.average_service_time = average_service_time
        self.num_cpus = num_cpus
        self.scenario = scenario
        self.processes_completed = 0
        self.clock = 0
        self.event_queue = queue.PriorityQueue()
        self.total_waiting_time = 0
        self.total_service_time = 0
        self.total_turnaround_time = 0
        self.total_processes_arrived = 0
        
        # Scenario-specific setup
        self.cpus = [CPU() for _ in range(num_cpus)]
        if scenario == 1:
            self.ready_queues = [queue.Queue() for _ in range(num_cpus)]
        else:
            self.global_ready_queue = queue.Queue()

        # Initialize CPU utilization logs
        self.cpu_utilization_logs = [[] for _ in range(num_cpus)]

    def run(self):
        # Start by scheduling the first process
        initial_process = self.generate_process(0)
        self.schedule_event("ARRIVAL", initial_process.arrival_time, initial_process)

        try:
            # Run the simulation until the end condition is met
            while not self.end_condition():
                if not self.event_queue.empty():
                    event = self.event_queue.get()
                    self.clock = event.event_time  # Synchronize simulation time to the event time

                    if event.event_type == "ARRIVAL":
                        self.handle_arrival(event)
                    elif event.event_type == "DEPARTURE":
                        self.handle_departure(event, event.cpu_index if hasattr(event, 'cpu_index') else None)
                else:
                    # Log or handle the situation where there are no more events but the end condition isn't met
                    print("Warning: Event queue is empty before end condition is met.")
                    break
        except Exception as e:
            print(f"An error occurred during simulation: {e}")

        # Report the final metrics once the simulation ends
        self.report_metrics()


    def handle_arrival(self, event):
        # Determine which scenario we are working with
        if self.scenario == 1:
            # Scenario 1: Every CPU has its own queue
            # Randomly select one of the CPU queues
            selected_cpu_index = random.randint(0, self.num_cpus - 1)
            selected_cpu = self.cpus[selected_cpu_index]
            selected_queue = self.ready_queues[selected_cpu_index]
            
            # If the selected CPU is busy, put the process in its queue
            if selected_cpu.is_busy:
                selected_queue.put(event.process)
            else:
                # If the CPU is idle, assign the process immediately
                departure_time = selected_cpu.assign_process(event.process, self.clock)
                self.schedule_event("DEPARTURE", departure_time, event.process, selected_cpu_index)
            
        elif self.scenario == 2:
            # Scenario 2: All CPUs share a global Ready Queue
            # Check if there is any idle CPU available
            idle_cpu_found = False
            for cpu_index, cpu in enumerate(self.cpus):
                if not cpu.is_busy:
                    # If a CPU is idle, assign the process immediately
                    departure_time = cpu.assign_process(event.process, self.clock)
                    self.schedule_event("DEPARTURE", departure_time, event.process, cpu_index)
                    idle_cpu_found = True
                    break
            
            if not idle_cpu_found:
                # If all CPUs are busy, put the process in the global queue
                self.global_ready_queue.put(event.process)
        
        # Regardless of the scenario, schedule the next arrival
        next_process = self.generate_process(self.clock)
        self.schedule_event("ARRIVAL", next_process.arrival_time, next_process)

    def handle_departure(self, event, cpu_index=None):
        if cpu_index is None:
            raise ValueError("CPU index must be provided for departure handling.")
        # Retrieve the CPU index from the event
        cpu_index = event.cpu_index

        # Update the simulator's clock to the event time
        self.clock = event.event_time

        # Release the process from the specified CPU and update utilization metrics
        self.cpus[cpu_index].release(self.clock)

        # Process the next steps based on the scenario
        if self.scenario == 1:
            # Scenario 1: Each CPU has its own ready queue
            self.process_departure_scenario1(cpu_index)
        elif self.scenario == 2:
            # Scenario 2: All CPUs share a single global ready queue
            self.process_departure_scenario2(cpu_index)

        # Update completion and performance metrics
        self.update_completion_metrics(event)

    def process_departure_scenario1(self, cpu_index):
        if not self.ready_queues[cpu_index].empty():
            next_process = self.ready_queues[cpu_index].get()
            departure_time = self.cpus[cpu_index].assign_process(next_process, self.clock)
            self.schedule_event("DEPARTURE", departure_time, next_process, cpu_index)

    def process_departure_scenario2(self, cpu_index):
        if not self.global_ready_queue.empty():
            next_process = self.global_ready_queue.get()
            departure_time = self.cpus[cpu_index].assign_process(next_process, self.clock)
            self.schedule_event("DEPARTURE", departure_time, next_process, cpu_index)

    def update_completion_metrics(self, event):
        self.processes_completed += 1
        self.total_service_time += event.process.service_time
        waiting_time = self.clock - event.process.arrival_time
        self.total_waiting_time += max(0, waiting_time - event.process.service_time)
        turnaround_time = self.clock - event.process.arrival_time
        self.total_turnaround_time += turnaround_time
    
    def generate_process(self, last_arrival_time):
        inter_arrival_time = random.expovariate(self.lambda_rate)
    
        # Calculate the new process's arrival time by adding the inter-arrival time to the last arrival time
        arrival_time = last_arrival_time + inter_arrival_time
        
        # Generate the service time using exponential distribution based on the average service time
        service_time = random.expovariate(1.0 / self.average_service_time)
        
        # Create a new process with the calculated arrival and service times
        new_process = Process(arrival_time, service_time)
        
        return new_process

    def end_condition(self):
        return self.processes_completed >= 10000

    def schedule_event(self, event_type, event_time, process, cpu_index=None):
        # Create a new event object with the provided parameters
        new_event = Event(event_type, event_time, process, cpu_index)

        # Put the new event into the priority queue
        # The Event class must implement comparison operators to maintain the queue's order correctly
        self.event_queue.put(new_event)


    def report_metrics(self):
        if self.processes_completed == 0:
            print("No processes completed. Metrics cannot be calculated.")
            return

        # Calculate average waiting time
        average_waiting_time = self.total_waiting_time / self.processes_completed

        # Calculate average turnaround time
        average_turnaround_time = self.total_turnaround_time / self.processes_completed

        # Calculate total throughput
        total_throughput = self.processes_completed / self.clock  # processes per unit time

        # Calculate average queue length based on scenario
        if self.scenario == 1:
            average_queue_lengths = [queue.qsize() for queue in self.ready_queues]
            print("Average Queue Lengths for Each CPU Queue:")
            for idx, length in enumerate(average_queue_lengths):
                print(f"CPU {idx + 1}: {length}")
        elif self.scenario == 2:
            average_queue_length = self.global_ready_queue.qsize()
            print(f"Average Queue Length for Global Queue: {average_queue_length}")

        # Calculate CPU utilization for each CPU
        print("CPU Utilizations:")
        for idx, cpu in enumerate(self.cpus):
            # Assume get_utilization is a method in CPU class that computes utilization based on total simulation time
            cpu_utilization = cpu.get_utilization(self.clock)
            print(f"CPU {idx + 1}: {cpu_utilization:.2f}%")

        # Print out other metrics
        print(f"Average Waiting Time: {average_waiting_time:.2f} units")
        print(f"Average Turnaround Time: {average_turnaround_time:.2f} units")
        print(f"Total Throughput: {total_throughput:.2f} processes per unit time")
