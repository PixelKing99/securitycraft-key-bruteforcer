from pyautogui import *
import pyautogui
import time
import keyboard
# import random
import win32api, win32con
# import colorama
# from datetime import datetime
from PIL import Image
import os


def left_click(x,y):
    win32api.SetCursorPos((x,y))
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def right_click():
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)

def countdown(current):

    while keyboard.is_pressed("esc") == False:

        i = len(current)-1
        
        while current[i] == 0:
            if i == 0:
# removes the last item
                current.pop()
                break
            i-=1
        if i != -1:
            current[i]-=1
        i+=1
        while i != len(current):
            current[i] = max_value
            i+=1

        combo = ""
        x = 0
        while x < len(current):
            new_char = character_list[current[x]]
            keyboard.press_and_release(new_char)
            combo+=new_char
            x+=1
        print(combo)
        time.sleep(2)
        if keyboard.is_pressed("q") == True or pause == True:
            print("paused")
            time.sleep(3)
            if require_input == True:
                input("press enter")
            while keyboard.is_pressed("q") == False or pause == True:
                time.sleep(1)
            print("unpaused")
            time.sleep(3)
        if pyautogui.pixel(1066,330)[0] != 0:
            if break_in_type == "item_frame":
                time.sleep(1)
                right_click()
            if leave_game == True:
                leave(break_in_type, combo)
            exit(combo)
        keyboard.press_and_release("enter")

def check_blacklisted_times():
    blacklisted_times =[]
    # did have 14 (2pm) but temp removed, 5, 10
    hour = list(time.localtime())[3]

    for t in blacklisted_times:
        if hour == t:
            time.sleep(1)
            if break_in_type != "chest":
                keyboard.press_and_release("esc")
            leave(break_in_type, combo)

def leave(break_in_type, combo):
# this just disconnects
    time.sleep(1)
    if break_in_type == "chest":
        keyboard.press_and_release("esc")
    time.sleep(1)
    keyboard.press_and_release("esc")
    time.sleep(1)
    left_click(961, 677)
    time.sleep(4)
    ss = pyautogui.screenshot()
    
    ss.save(os.path.join(dirname, str(combo)+'two.png'))
    exit(combo)
def breifcase():
    max_value = 9
    current = [0, 0, 0, 0]
    while keyboard.is_pressed("esc") == False and pyautogui.pixel(1002,491)[0] == 0:
        i = 3
        # time.sleep(0.005)
        print(current)
        keyboard.press_and_release("tab")
        time.sleep(0.001)
        keyboard.press_and_release("tab")
        time.sleep(0.001)
        keyboard.press_and_release("enter")
        time.sleep(0.001)
        keyboard.press_and_release("shift+tab")
        time.sleep(0.001)
        keyboard.press_and_release("shift+tab")
        time.sleep(0.001)
        while current[i] == max_value and keyboard.is_pressed("esc") == False:
            keyboard.press_and_release("enter")
            current[i] = 0
            print(current)
            time.sleep(0.001)
            keyboard.press_and_release("shift+tab")
            time.sleep(0.001)
            keyboard.press_and_release("shift+tab")
            time.sleep(0.001)
            i-=1
        keyboard.press_and_release("enter")
        current[i] += 1
        print(i)
        while i < 3 and keyboard.is_pressed("esc") == False:
            keyboard.press_and_release("tab")
            time.sleep(0.001)
            keyboard.press_and_release("tab")
            time.sleep(0.001)
            i+=1


require_input = True
pause = False
leave_game = True
break_in_type = "breifcase"
# chest
# door
# item_frame
# breifcase
arrow_y = 402
arrow_position = [874, 930, 993, 1046]
enter_arrow = [1110, 473]

# character_list = ["1","2","3","4","5"]
character_list = ["0","1","2","8","3","4","5","6","7","9"]
# character_list = ["0","1","2","3","4","5","6","7","8","9"]

max_value = len(character_list)-1

current = [0]

input("press enter")
print("starting in 5")
time.sleep(5)
if break_in_type == "breifcase":
    breifcase()
    exit()
left_click(870, 383)
time.sleep(0.5)
left_click(1046, 676)
# print(current[-1])

while keyboard.is_pressed("esc") == False:

# makes i start at the end of the list of numbers
    i = len(current)-1

# cycles through the values until it finds one that is not at its max
# in 1249999 that would be the 4
# in 17 that would be 7
    while current[i] == max_value:
# if the next value to be increased is the first one
        if i == 0:
# adds a 0 onto the end then skips checking the value in front of it b/c that would break it
            current.append(character_list[0])
        i-=1
# this is here so that every once in a while it checks if it should leave because my ops are likely to be on
        if leave_game == True:
            if len(current) >=3:
                if current[-3] == character_list[0]:
                    check_blacklisted_times()
# increases the value in front of the maxed values by one
# from 1249999 to 1259999
    if i != -1:
        current[i]+=1
# moves the selected value from 12'5'9999 to 125'9'999
    i+=1
# until the selected value is is the last one it sets the current value to 0 and moves towards the end
    while i != len(current):
        current[i] = 0
        i+=1

    combo = ""
    x = 0
# printing/ using the combo of numbers
    while x < len(current):
        new_char = character_list[current[x]]
        keyboard.press_and_release(new_char)
        combo+=new_char
        x+=1
    print(combo)
    time.sleep(0.042)
    if keyboard.is_pressed("q") == True or pause == True:
        print("paused")
        time.sleep(3)
        if require_input == True:
            input("press enter")
        while keyboard.is_pressed("q") == False or pause == True:
            time.sleep(1)
        print("unpaused")
        time.sleep(3)
    if pyautogui.pixel(1066,330)[0] != 0:
        time.sleep(0.5)
        ss = pyautogui.screenshot()
        ss.save(os.path.join(dirname, str(combo)+'one.png'))
        time.sleep(1)
        if break_in_type == "chest":
            keyboard.press_and_release("esc")
        if break_in_type == "item_frame":
            right_click()
        time.sleep(3)
        right_click()
        time.sleep(0.5)
        left_click(870, 383)
        time.sleep(0.5)
        left_click(1046, 676)
        time.sleep(0.5)
        countdown(current)
    keyboard.press_and_release("enter")