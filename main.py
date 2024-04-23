# To run use command python main.py <lambda_rate> <average_service_time>
# Where <lambda_rate> and <average_service_time> must be 10 and 0.04 respectively.
import sys
from simulator import Simulator

def main():
    if len(sys.argv) != 3:
        print("Incorrect Usage. Valid input contains exactly 3 arguments as follows:")
        print("Correct Usage: python main.py <lambda_rate> <average_service_time>")
        print("Correct Usage: python main.py 10 0.04")
        sys.exit(1)

    try:
        lambda_rate = float(sys.argv[1])
        average_service_time = float(sys.argv[2])

        if lambda_rate != 10 or average_service_time != 0.04:
            raise ValueError
    
    except ValueError:
        print("Invalid input. <lambda_rate> and <average_service_time>" +
        " must be 10 and 0.04 respectively.")
        sys.exit(1)

    while lambda_rate < 31:
        print("Results for lambda rate of " + str(lambda_rate) + ":")
        simulator = Simulator(lambda_rate, average_service_time)
        simulator.run()
        lambda_rate += 1
        print()

if __name__ == "__main__":
    main()
