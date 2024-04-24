# MM4 Queue Simulation
#
# To run use command python main.py <lambda_rate> <average_service_time> <scenario> <num_cpus>
# Where <lambda_rate> is 50, <average_service_time> is 0.02, <scenario> is 1 or 2 <num_cpus> is 4.
#
# command to simulate scenario 1: python main.py 50 0.02 1 4
# command to simulate scenario 2: python main.py 50 0.02 2 4

import sys
from multi_cpu_simulator import MultiCPUSimulator

def main():
    if len(sys.argv) != 5:
        print("Usage: python main.py <lambda_rate> <average_service_time> <scenario> <num_cpus>")
        sys.exit(1)

    try:
        lambda_rate = int(sys.argv[1])
        average_service_time = float(sys.argv[2])
        scenario = int(sys.argv[3])
        num_cpus = int(sys.argv[4])

        if scenario not in [1, 2]:
            raise ValueError("Scenario must be 1 or 2.")
        if num_cpus != 4:
            raise ValueError("Number of CPUs must be 4.")
        if lambda_rate != 50:
            raise ValueError("Lambda rate must be 50 processes per second.")
        if average_service_time != 0.02:
            raise ValueError("Average service time must be 0.02.")

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    for rate in range(50, 151, 10):
        print(f"\nRunning simulation with Lambda Rate: {rate}, Scenario: {scenario}, CPUs: {num_cpus}")
        simulator = MultiCPUSimulator(rate, average_service_time, num_cpus, scenario)
        simulator.run()

if __name__ == "__main__":
    main()