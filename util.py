import pyautogui
import time
import keyboard

from consts import *

def left_click(c):
    if DEBUG: print(f"clicking {c[0]} {c[1]}")
    pyautogui.click(c[0], c[1])

# this will be buggy if 'raw input' is on in your mouse settings
def right_click():
    pyautogui.click(button="right")


# this one seems to work no matter what but is slower
def press(char):
    # keyboard.press_and_release(char) # in my tests this took like no time (<0.01), but it isnt reliable in the briefcase gui
    pyautogui.press(char) # in my tests this took like 0.1 seconds

# this one only seems to work after the buttons have been pressed a couple times using the other method which makes it jank to use but idk
def fastpress(char):
    # these sleep values were the smallest i could get to work in testing, if the buttons are failing to be pressed then you may want to test until you get values that work for you or you should just use the press() method
    time.sleep(0.03)
    keyboard.press_and_release(char)
    time.sleep(0.01)

def isPressed(char):
    return keyboard.is_pressed(char)



def screenShot(name):
    ss = pyautogui.screenshot()
    
    ss.save("./images/"+name+".png")




# converts the numbers used to represent the currentCombo into the characters assign to them in character_list
def comboToString(comboArray, character_list):
    combo = ""
    for val in comboArray:
        combo += character_list[val]
    return combo


def checkExitKey():
    return isPressed("space") or isPressed("esc") or isPressed("s")



def check_blacklisted_times():
    hour = list(time.localtime())[3]
    if DEBUG: print("hour:", hour)

    return hour in BLACKLISTED_TIMES