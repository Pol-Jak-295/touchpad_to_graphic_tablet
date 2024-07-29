import keyboard
import evdev
from evdev import InputDevice, categorize, ecodes
import subprocess
import signal
import sys

absolutify = False


# Adjust these values based on your screen resolution and touchpad size
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
TOUCHPAD_WIDTH = 3180  # example values, you may need to adjust these
TOUCHPAD_HEIGHT = 2080  # example values, you may need to adjust these


# Get the device
device = InputDevice('/dev/input/event6')  # change this to your touchpad device

# Helper function to map touchpad coordinates to screen coordinates
def map_value(value, in_min, in_max, out_min, out_max):
    return max(0, (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min - 10)

print("Press F6 to toggle between touchpad and graphic tablet mode")
def on_key_press(event):
    global absolutify
    if event.name == 'f6':
        absolutify = not absolutify
        print("F6 key pressed!")
        print("absolitify is now:", absolutify)


        if absolutify:


            # Disable the touchpad
            subprocess.run(['xinput', 'disable', '15'])  # change this to your touchpad id


            for event in device.read_loop():
                if event.type == ecodes.EV_ABS:
                    absevent = categorize(event)
                    if absevent.event.code == ecodes.ABS_X:
                        x = map_value(absevent.event.value, 0, TOUCHPAD_WIDTH, 0, SCREEN_WIDTH)
                    if absevent.event.code == ecodes.ABS_Y:
                        y = map_value(absevent.event.value, 0, TOUCHPAD_HEIGHT, 0, SCREEN_HEIGHT)
                        subprocess.run(['xdotool', 'mousemove', str(int(x)), str(int(y))])
        else:
            # Enable the touchpad
            subprocess.run(['xinput', 'enable', '15'])
    else:
        pass
    

# Signal handler for SIGINT
def signal_handler(sig, frame):
    print(f'\n Ctrl+C received! Re-enabling the touchpad...')
    subprocess.run(['xinput', 'enable', '15'])  # change this to your touchpad id
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)




keyboard.on_press(on_key_press)

# Keep the program running
keyboard.wait()
