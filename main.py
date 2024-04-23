import sys
from multi_cpu_simulator import MultiCPUSimulator

def main():
    # Check if the correct number of arguments are provided
    if len(sys.argv) != 5:
        print("Usage: python main.py <lambda_rate> <average_service_time> <scenario> <num_cpus>")
        sys.exit(1)

    try:
        # Parse command-line arguments
        lambda_rate = float(sys.argv[1])
        average_service_time = float(sys.argv[2])
        scenario = int(sys.argv[3])
        num_cpus = int(sys.argv[4])

        # Validate the inputs
        if scenario not in [1, 2]:
            raise ValueError("Scenario must be 1 or 2.")
        if num_cpus < 1:
            raise ValueError("Number of CPUs must be at least 1.")
        if lambda_rate < 50 or lambda_rate > 150:
            raise ValueError("Lambda rate must be between 50 and 150 processes per second.")
        if average_service_time <= 0:
            raise ValueError("Average service time must be positive.")

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Run the simulation for each lambda rate in steps of 10 from 50 to 150
    for rate in range(50, 151, 10):
        print(f"\nRunning simulation with Lambda Rate: {rate}, Scenario: {scenario}, CPUs: {num_cpus}")
        simulator = MultiCPUSimulator(rate, average_service_time, num_cpus, scenario)
        simulator.run()

if __name__ == "__main__":
    main()