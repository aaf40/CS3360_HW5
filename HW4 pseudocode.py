# while loop to manage event (arrivals, and departures)

while (!endCondition){
       
       event = get_event();
       clock = event.time;

       switch(event.type):
       
            case ARRIVAL:
                handle_arrival();
            case DEPARTURE:
                handle_departure();     
}
    
# handle_arrival method
    
handle_arrival(event){
    if(CPU_busy == 0) {
        CPU_busy = 1;
        schedule_event(DEPARTURE, clock + service_time, p)
    }
    else {
        add p to ready queue;
        schedule_event(ARRIVAL, clock + interrival_time, next_process)
    }
}

# handle_arrival method

handle_departure(event) {
    if (Ready_Queue is empty == 1){
        CPU_busy = 0;
    }
    else {
        p = get_next_from Ready_Queue
        schedule_event(DEPARTURE, clock + service_time, p)
    }
}
