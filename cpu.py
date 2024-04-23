class CPU:
    def __init__(self):
        self.is_busy = False
        self.current_process = None
        self.utilization_time = 0
        self.last_start_time = None  # To track when the current process started

    def assign_process(self, process, current_time):
        process.start_time = current_time  # Adding this line to update start time
        self.current_process = process
        self.is_busy = True
        self.last_start_time = current_time  # Start time of the process
        return current_time + process.service_time


    def release(self, current_time):
        if self.current_process:
            self.utilization_time += current_time - self.last_start_time
            self.current_process = None
        self.is_busy = False
        self.last_start_time = None

    def get_utilization(self, total_simulation_time):
        return (self.utilization_time / total_simulation_time) * 100
