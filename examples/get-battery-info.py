from pthub import pthub
from time import sleep


pthub.initialise()

pthub.start()

while True:

    charging_state, capacity, time, power = pthub.get_battery_state()
    print("charging_state: " + str(charging_state))
    print("time: " + str(time))
    print("capacity: " + str(capacity))

    print("----------")

    sleep(1)
