class CPU:
    def __init__(self):
        self.is_busy = False  # CPU starts as idle
        self.current_process = None  # No process is currently being serviced
        self.utilization_time = 0  # Track how long the CPU has been utilized

    def assign_process(self, process, current_time):
        """
        Assign a process to the CPU and mark it as busy.
        """
        self.current_process = process
        self.is_busy = True
        # Schedule a departure event based on the service time of the process
        departure_time = current_time + process.service_time
        return departure_time  # This will be used to schedule the departure event

    def release(self, current_time):
        """
        Release the current process and mark CPU as idle.
        """
        if self.current_process:
            # Calculate the time the process spent running on the CPU
            process_run_time = current_time - (self.current_process.arrival_time + self.current_process.wait_time)
            self.utilization_time += process_run_time
            self.current_process = None
        self.is_busy = False

    def get_utilization(self, total_simulation_time):
        """
        Calculate the utilization percentage of the CPU.
        """
        if self.is_busy:
            # If the CPU is busy, account for the ongoing process
            self.utilization_time += total_simulation_time - self.current_process.arrival_time
        return (self.utilization_time / total_simulation_time) * 100
