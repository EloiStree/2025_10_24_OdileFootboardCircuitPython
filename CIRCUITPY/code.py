# ----------------------------------------------------------------------------
# Raspberry Pi Pico - HID Keyboard + Mouse Input with Debouncing
# ----------------------------------------------------------------------------
# Source of the code:
# https://github.com/EloiStree/2025_10_24_OdileFootboardCircuitPython
# LICENSE: https://github.com/EloiStree/License
# ----------------------------------------------------------------------------

import sys
import time
import board
import digitalio
import usb_hid
from adafruit_debouncer import Debouncer
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

# -------------------------------------------------------------------------
# Basic Info
# -------------------------------------------------------------------------
print("Hello, CircuitPython!")
print(f"sys.implementation: {sys.implementation}")
print(f"sys.version: {sys.version}")
print(f"sys.platform: {sys.platform}")

# -------------------------------------------------------------------------
# Initialize HID Devices
# -------------------------------------------------------------------------
keyboard = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)

# -------------------------------------------------------------------------
# Setup Buttons (with internal pull-ups)
# -------------------------------------------------------------------------
# NOTE: Use GPIO numbers, not physical pin numbers.
# Connect one side of each button to GND, and the other to the GPIO below.

button_a_pin = digitalio.DigitalInOut(board.GP26)  # Button A → single click
button_a_pin.direction = digitalio.Direction.INPUT
button_a_pin.pull = digitalio.Pull.UP
button_a = Debouncer(button_a_pin)

button_b_pin = digitalio.DigitalInOut(board.GP11)  # Button B → triple click
button_b_pin.direction = digitalio.Direction.INPUT
button_b_pin.pull = digitalio.Pull.UP
button_b = Debouncer(button_b_pin)

button_c_pin = digitalio.DigitalInOut(board.GP4)   # Button C → Enter key
button_c_pin.direction = digitalio.Direction.INPUT
button_c_pin.pull = digitalio.Pull.UP
button_c = Debouncer(button_c_pin)

# -------------------------------------------------------------------------
# Mouse & Keyboard Functions
# -------------------------------------------------------------------------

def func_odile_click():
    """Single mouse click."""
    print("Mouse single click")
    mouse.click(Mouse.LEFT_BUTTON)

def func_odile_triple_click():
    """Triple mouse click."""
    print("Mouse triple click")
    for i in range(3):
        mouse.click(Mouse.LEFT_BUTTON)
        time.sleep(0.1)  # small delay between clicks

def func_odile_enter():
    """Keyboard Enter press."""
    print("Keyboard ENTER")
    keyboard.press(Keycode.ENTER)
    time.sleep(0.05)
    keyboard.release(Keycode.ENTER)


def on_change_button_a(new_value_pressing: bool):
    print(f"Button A changed to: {new_value_pressing}")
    if new_value_pressing == False:
        func_odile_click()

def on_change_button_b(new_value_pressing: bool):
    print(f"Button B changed to: {new_value_pressing}")
    if new_value_pressing == False:
        func_odile_enter()

def on_change_button_c(new_value_pressing: bool):
    print(f"Button C changed to: {new_value_pressing}")
    #on release
    if new_value_pressing == False:
        func_odile_triple_click()


# -------------------------------------------------------------------------
# Main Loop
# -------------------------------------------------------------------------
print("Ready! Press your buttons...")

while True:
    # Update debounced states
    button_a.update()
    button_b.update()
    button_c.update()

    # ----- Button A (GPIO26) -----
    if button_a.fell:
        on_change_button_a(True)
    if button_a.rose:
        on_change_button_a(False)

    # ----- Button B (GPIO11) -----
    if button_b.fell:
        on_change_button_b(True)
    if button_b.rose:
        on_change_button_b(False)

    # ----- Button C (GPIO4) -----
    if button_c.fell:
        on_change_button_c(True)
    if button_c.rose:
        on_change_button_c(False)

    time.sleep(0.01)  # Small loop delay for stability

