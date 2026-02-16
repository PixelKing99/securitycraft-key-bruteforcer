import pyautogui
import time
import utils as u

# uses the mouse to press the arrows instead of using the tab keys to navigate due to the fact that making sure the tab presses register is quite slow
USE_FAST_BRIEFCASE_MODE = True

# 'enum' of bruteforce types
CHEST = 0
BRIEFCASE = 1
ITEM_FRAME = 2
DOOR = 3


# for saving mouse coordinates to use in the macro
def getMousePosition(message):
    print(message)
    print("press enter once your mouse is in the correct position")
    while not u.isPressed("enter"):
        time.sleep(0.05)
    position = pyautogui.position()
    print(position[0], position[1])
    time.sleep(1)
    return position

# for saving a mouse coordinate that is expected to be a specific color, this makes sure the user did not mess up their selection
def getCheckedMousePosition(message, expectedColorName, expectedRedValue):
    print(message)
    isCorrect = False
    while not isCorrect:
        print("press enter once your mouse is in the correct position")
        while not u.isPressed("enter"):
            time.sleep(0.05)
        position = pyautogui.position()
        print(position[0], position[1])
        time.sleep(1)
        
        isCorrect = pyautogui.pixel(position[0],position[1])[0] == expectedRedValue
        if not isCorrect:
            print(f"the position you selected is not {expectedColorName} and therefore cannot be the correct pixel, try again")
    time.sleep(1)
    return position


def getPositions(BREAK_IN_TYPE):
    NUM_OF_COORDS = 10

    disconnect = None
    topRightOfChest = None
    showPasscode = None
    briefcaseCheck = None
    briefcaseDownArrow = None
    briefcaseArrows = [None,None,None,None]
    briefcaseEnter = None


    prevPositions = [None for _ in range(NUM_OF_COORDS)]

    try:
        with open("settings.txt", "x") as f:
            f.write("\n" * NUM_OF_COORDS)
    except FileExistsError:
        pass

    with open("settings.txt", "r") as f:
        lines = f.readlines()
        
        for i in range(min(len(lines), NUM_OF_COORDS)):
            line = lines[i].split(",")
            if len(line) == 2:
                prevPositions[i] = (int(line[0]), int(line[1]))

    print(prevPositions)
    usePrev = input("would you like to use the saved previous positions (Y/n)\n") != "n"
    

    if usePrev and prevPositions[0]:
        disconnect = prevPositions[0]
    else:
        disconnect = getMousePosition("hover your mouse over the disconnect button")


    if usePrev and prevPositions[1]:
        topRightOfChest = prevPositions[1]
    elif BREAK_IN_TYPE != BRIEFCASE:
        m = "place your mouse just inside the top right corner of the chest input. make sure it is over the black part\nif you want to know the exact valid area, fill the text box with values (with show passcode on) and it is the area where no character are able to be"
        topRightOfChest = getCheckedMousePosition(m, "black", 0) # the top right of the text box for the chest etc is where this should be (where it is black), also using this to select the input box
            

    if usePrev and prevPositions[2]:
        showPasscode = prevPositions[2]
    elif BREAK_IN_TYPE != BRIEFCASE:
        showPasscode = getMousePosition("hover your mouse over the 'show passcode' button")


    if usePrev and prevPositions[3]:
        briefcaseCheck = prevPositions[3]
    elif BREAK_IN_TYPE == BRIEFCASE:
        briefcaseCheck = getCheckedMousePosition("hover your mouse over the black space beside one of the numbers in the briefcase", "black", 0)


    if usePrev and prevPositions[4]:
        briefcaseDownArrow = prevPositions[4]
    elif BREAK_IN_TYPE == BRIEFCASE:
        briefcaseDownArrow = getMousePosition("hover your mouse over the first down arrow on the right in the briefcase")

    for i in range(0,4):
        if usePrev and prevPositions[5+i]:
            briefcaseArrows[i] = prevPositions[5+i]
        elif BREAK_IN_TYPE == BRIEFCASE and USE_FAST_BRIEFCASE_MODE == True:
            briefcaseArrows[i] = getMousePosition(f"if the briefcase's up arrows were numbered 1,2,3,4 from the left, hover your mouse over the up arrow in the '{i+1}' position")


    if usePrev and prevPositions[9]:
        briefcaseEnter = prevPositions[9]
    elif BREAK_IN_TYPE == BRIEFCASE and USE_FAST_BRIEFCASE_MODE == True:
        briefcaseEnter = getMousePosition("hover your mouse over the enter button in the briefcase")

    
    lines = [
        f"{disconnect[0]},{disconnect[1]}\n" if disconnect else "\n",
        f"{topRightOfChest[0]},{topRightOfChest[1]}\n" if topRightOfChest else "\n",
        f"{showPasscode[0]},{showPasscode[1]}\n" if showPasscode else "\n",
        f"{briefcaseCheck[0]},{briefcaseCheck[1]}\n" if briefcaseCheck else "\n",
        f"{briefcaseDownArrow[0]},{briefcaseDownArrow[1]}\n" if briefcaseDownArrow else "\n",
        f"{briefcaseArrows[0][0]},{briefcaseArrows[0][1]}\n" if briefcaseArrows[0] else "\n",
        f"{briefcaseArrows[1][0]},{briefcaseArrows[1][1]}\n" if briefcaseArrows[1] else "\n",
        f"{briefcaseArrows[2][0]},{briefcaseArrows[2][1]}\n" if briefcaseArrows[2] else "\n",
        f"{briefcaseArrows[3][0]},{briefcaseArrows[3][1]}\n" if briefcaseArrows[3] else "\n",
        f"{briefcaseEnter[0]},{briefcaseEnter[1]}\n" if briefcaseEnter else "\n",
    ]

    with open("settings.txt", "w") as f:
        f.writelines(lines)


    return disconnect, topRightOfChest, showPasscode, briefcaseCheck, briefcaseDownArrow, briefcaseArrows, briefcaseEnter