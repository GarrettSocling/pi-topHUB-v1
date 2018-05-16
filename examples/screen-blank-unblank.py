from pthub import pthub
from time import sleep


def print_screen_state_str():
    current_screen_off_state_bit = pthub.get_screen_off_state()
    if current_screen_off_state_bit == 1:
        current_screen_off_state = "blanked"
    else:
        current_screen_off_state = "unblanked"

    print("Current screen state: " + current_screen_off_state)


pthub.initialise()
print("Current device: " + pthub.get_device_id())

print_screen_state_str()

print("Blanking screen...")
pthub.blank_screen()

print_screen_state_str()

print("Waiting 5 seconds...")
sleep(5)

print("Unblanking screen...")
pthub.unblank_screen()

print_screen_state_str()
