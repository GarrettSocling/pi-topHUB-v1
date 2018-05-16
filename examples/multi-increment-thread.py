from pthub import pthub
from time import sleep


pthub.initialise()
print("Current device: " + pthub.get_device_id())

print("Starting thread...")
pthub.start()

print("Setting brightness to 50%...")
pthub.set_brightness(5)

for i in range(5):

    print("Waiting 2 seconds...")
    sleep(2)

    print("Incrementing brightness...")
    pthub.increment_brightness()


print("Stopping thread...")
pthub.stop()
print("Done")
