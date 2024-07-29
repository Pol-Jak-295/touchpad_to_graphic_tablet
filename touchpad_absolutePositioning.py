# Title: Touchpad -> graphic tablet
# Description: Use your touchpad as a graphic tablet
# Author: Jaka Polesnik
# Date: 2021-09-29
# Code version: 1.0
# Python version: 3.12.3
# License: MIT
#
# This script allows you to use your touchpad as a graphic tablet. No rocket science, just a simple script that can be useful for some people, and fun to play with for the others.


import keyboard
import subprocess
import signal
import sys
import threading
from evdev import InputDevice, categorize, ecodes






# Configuration
# Configure the values below
# Those are things that might need to be changed for your usage
# Adjust these values based on your screen resolution and touchpad size
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
TOUCHPAD_WIDTH = 3180  # Values that worked for me, you may need to adjust these
TOUCHPAD_HEIGHT = 2080  # Values that worked for me, you may need to adjust these
TOUCHPAD_ID = 15  # Change this to your touchpad ID
DEVICE_PATH = '/dev/input/event6'  # Change this to your touchpad device path
KEYBIND = 'f6'

# Please check before posting that it doesn’t work
# Please change those values above before telling me it doesn’t work
# I believe in you, you can do it :D
# Do not forget to change the id of the touchpad to your touchpad id
# Please check before posting that it doesn’t work
# Please, please, please
# I don’t want to be mean but please
# Please
# Please
# I don’t want stupid bug reports, so please check you’ve changed all the values before posting
# My code is broken
# Please, for the love of god
# Please




# Global flag to toggle mode
absolutify_value = False

def map_value(value, in_min, in_max, out_min, out_max):
    return max(0, (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

print(f'toggling the script on and off uses the keybind: {KEYBIND}')
def on_key_press(event):
    global absolutify_value
    if event.name == KEYBIND:
        absolutify_value = not absolutify_value
        print(f"{KEYBIND} key pressed! Absolutify is now:", absolutify_value)
        toggle_mode(absolutify_value)

def toggle_mode(enable_graphic_tablet):
    if enable_graphic_tablet:
        try:
            subprocess.run(['xinput', 'disable', str(TOUCHPAD_ID)], check=True)
            print('Current mode: Graphic tablet mode')
            listen_for_touchpad_events()
        except subprocess.CalledProcessError:
            print(f"Error: Failed to disable touchpad with ID {TOUCHPAD_ID}.")
            print("Please check the configuration section to ensure the TOUCHPAD_ID is correct.")
    else:
        try:
            subprocess.run(['xinput', 'enable', str(TOUCHPAD_ID)], check=True)
            print('Current mode: Touchpad mode')
        except subprocess.CalledProcessError:
            print(f"Error: Failed to enable touchpad with ID {TOUCHPAD_ID}.")
            print("Please check the configuration section to ensure the TOUCHPAD_ID is correct.")

def listen_for_touchpad_events():
    try:
        device = InputDevice(DEVICE_PATH)
        for event in device.read_loop():
            if event.type == ecodes.EV_ABS:
                absevent = categorize(event)
                if absevent.event.code == ecodes.ABS_X:
                    x = map_value(absevent.event.value, 0, TOUCHPAD_WIDTH, 0, SCREEN_WIDTH)
                elif absevent.event.code == ecodes.ABS_Y:
                    y = map_value(absevent.event.value, 0, TOUCHPAD_HEIGHT, 0, SCREEN_HEIGHT)
                    subprocess.run(['xdotool', 'mousemove', str(int(x)), str(int(y))], check=True)
    except FileNotFoundError:
        print(f"Error: Device at {DEVICE_PATH} not found.")
        print("Please check the configuration section to ensure the DEVICE_PATH is correct.")
        sys.exit(1)
    except Exception as e:
        print(f"Error in touchpad event handling: {e}")

def signal_handler(sig, frame):
    print('\nCtrl+C received! Re-enabling the touchpad...')
    try:
        subprocess.run(['xinput', 'enable', str(TOUCHPAD_ID)], check=True)
        print('Touchpad re-enabled!')
    except subprocess.CalledProcessError:
        print(f"Error: Failed to enable touchpad with ID {TOUCHPAD_ID}.")
        print("Please check the configuration section to ensure the TOUCHPAD_ID is correct.")
    sys.exit(0)

# Set up signal handler
signal.signal(signal.SIGINT, signal_handler)

# Start keyboard listener in a separate thread
listener_thread = threading.Thread(target=keyboard.wait)
listener_thread.start()

# Register the key press event handler
keyboard.on_press(on_key_press)

# Keep the program running
keyboard.wait()
