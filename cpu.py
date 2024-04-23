class CPU:
    def __init__(self):
        self.is_busy = False
        self.current_process = None
        self.utilization_time = 0
        self.last_process_start_time = None  # Record when the last process started

    def assign_process(self, process, current_time):
        self.current_process = process
        self.is_busy = True
        self.last_process_start_time = current_time  # Start timing the process
        return current_time + process.service_time

    def release(self, current_time):
        if self.current_process:
            self.utilization_time += (current_time - self.last_process_start_time)
            self.current_process = None
        self.is_busy = False
        self.last_process_start_time = None  # Reset start time

    def get_utilization(self, total_simulation_time):
        # Only add ongoing process time if CPU is still busy
        ongoing_time = (total_simulation_time - self.last_process_start_time) if self.is_busy else 0
        return ((self.utilization_time + ongoing_time) / total_simulation_time) * 100
