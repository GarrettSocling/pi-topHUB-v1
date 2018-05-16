from pthub import pthub
from time import sleep


pthub.initialise()
print("Current device: " + pthub.get_device_id())

print("Setting brightness to 100%...")
pthub.set_brightness(10)


for i in range(5):
    brightness = pthub.get_brightness()
    print("BEFORE: " + str(brightness))

    print("Decrement brightness: " + str(i + 1) + "/5...")
    pthub.decrement_brightness()

    sleep(pthub.spi_cycle_sleep_time)

    brightness = pthub.get_brightness()
    print("AFTER: " + str(brightness))

    sleep(pthub.spi_cycle_sleep_time)


for i in range(5):
    brightness = pthub.get_brightness()
    print("BEFORE: " + str(brightness))

    print("Increment brightness: " + str(i + 1) + "/5...")
    pthub.increment_brightness()

    sleep(pthub.spi_cycle_sleep_time)

    brightness = pthub.get_brightness()
    print("AFTER: " + str(brightness))

    sleep(pthub.spi_cycle_sleep_time)
