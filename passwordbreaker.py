import pyautogui
import time
import keyboard

PASSCODE_COOLDOWN = 0.250 # default value in the server config for passcode_check_cooldown is 0.250
# from my tests in singleplayer you need about +0.07 to not get rate limited at all (idk why, lag or smthn), however down to 0.06 or so you can only get rate limited once in a while

LEAVE_ON_SUCCESS = True

BLACKLISTED_TIMES=[18]

# basically makes it so that on the first passcode entry it uses the default slow keypress method and then subsequently uses the fast method since for some reason that works
# if keypresses are failing to register then you should turn this off maybe, but then pressing buttons will be slower
OPTIMIZE_KEY_PRESSES = True

# uses the mouse to press the arrows instead of using the tab keys to navigate due to the fact that making sure the tab presses register is quite slow
USE_FAST_BRIEFCASE_MODE = True

DEBUG = False

CHEST = 0
BRIEFCASE = 1
ITEM_FRAME = 2
DOOR = 3










# default
DEFAULT_CHAR_LIST = ["0","1","2","3","4","5","6","7","8","9"]

# shorter just to use in testing 
TESTING_CHAR_LIST = ["1","2","3","4","5"]

# optimized, 8 is closer to the beginning cause people seemed to use it more often
OPTIMIZED_CHAR_LIST_1 = ["0","1","2","8","3","4","5","6","7","9"]

# from my 'testing' here is the count of times each number was the first digit
# having a + in between it means that is the number of times it was used exclusively as a briefcase password, which is significant cause you cant type briefcase passcodes and instead have to use arrows to increment etc the values so some will be easier to type than others, making the passcode potentially biased towards easy to type combos
# 0: 5 + 1
# 1: 19 + 1
# 2: 8
# 3: 3 + 1
# 4: 4
# 5: 4 + 1
# 6: 4
# 7: 2
# 8: 4
# 9: 1 + 1
# based off this data here is the 'technically' most optimized order (including briefcase codes)
OPTIMIZED_CHAR_LIST_2 = ["1","2","0","5","4","6","8","3","7","9"]






def left_click(x,y):
    if DEBUG: print(f"clicking {x} {y}")
    pyautogui.click(x, y)

# this will be buggy if 'raw input' is on in your mouse settings
def right_click():
    pyautogui.click(button='right')


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

def getMousePosition(message):
    print(message)
    print("press enter once your mouse is in the correct position")
    while not isPressed("enter"):
        time.sleep(0.05)
    position = pyautogui.position()
    print(position[0], position[1])
    time.sleep(1)
    return position

def getCheckedMousePosition(message, expectedColorName, expectedRedValue):
    print(message)
    isCorrect = False
    while not isCorrect:
        print("press enter once your mouse is in the correct position")
        while not isPressed("enter"):
            time.sleep(0.05)
        position = pyautogui.position()
        print(position[0], position[1])
        time.sleep(1)
        
        isCorrect = pyautogui.pixel(position[0],position[1])[0] == expectedRedValue
        if not isCorrect:
            print(f"the position you selected is not {expectedColorName} and therefore cannot be the correct pixel, try again")
    time.sleep(1)
    return position


def getPositions():
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



breakInType = int(input(f"enter the number corrospoding to what you are bruteforcing:\n{CHEST}. chest\n{BRIEFCASE}. briefcase\n{ITEM_FRAME}. item frame\n{DOOR}. door\n"))

if breakInType in [CHEST, BRIEFCASE, ITEM_FRAME, DOOR]:
    BREAK_IN_TYPE = breakInType
    if BREAK_IN_TYPE == BRIEFCASE:
        additional_delay = 0.18
    else:
        additional_delay = 0.08
else:
    exit("invalid option")

ADDITIONAL_DELAY = additional_delay


DISCONNECT_BUTTON, TOP_RIGHT_OF_CHEST_INPUT, SHOW_PASSCODE, BRIEFCASE_CHECK_POS, BRIEFCASE_DOWN_ARROW, BRIEFCASE_ARROWS, BRIEFCASE_ENTER = getPositions()


def breakIn():
    print("press 'space' or 'esc' to stop bruteforcing or 'q' to pause")
    print("starting in 5")
    time.sleep(5)



    if BREAK_IN_TYPE == CHEST or BREAK_IN_TYPE == ITEM_FRAME or BREAK_IN_TYPE == DOOR:
        
        left_click(SHOW_PASSCODE[0], SHOW_PASSCODE[1])
        time.sleep(0.1)
        left_click(TOP_RIGHT_OF_CHEST_INPUT[0], TOP_RIGHT_OF_CHEST_INPUT[1])

        CHAR_LIST = OPTIMIZED_CHAR_LIST_2

        success, combo = iterate(callback=chestCallback, exitCondition=checkExitKey, character_list=CHAR_LIST, maxlen=5)
        comboStr = comboToString(combo, CHAR_LIST)


    elif BREAK_IN_TYPE == BRIEFCASE:
        if USE_FAST_BRIEFCASE_MODE == True:
            
            left_click(BRIEFCASE_DOWN_ARROW[0], BRIEFCASE_DOWN_ARROW[1])
            currentCallback = fastBriefcaseCallback
            pass
        else:

            # this sets up the briefcase so that we can use tab and shift+tab to navigate the arrows
            left_click(BRIEFCASE_DOWN_ARROW[0], BRIEFCASE_DOWN_ARROW[1])
            pyautogui.keyDown('shift')
            pyautogui.press("tab")
            pyautogui.keyUp('shift')
            currentCallback = slowBriefcaseCallback


        # i need to make sure i dont set the character list to anything other than the default cause i cant change the order i enter the numbers in with the briefcase
        success, combo = iterate(startingValues=[0,0,0,0], maxlen=4, callback=currentCallback, exitCondition=checkExitKey)
        comboStr = comboToString(combo, DEFAULT_CHAR_LIST)
    
    
    
    if success:

        print("the passcode should be one of the ones which was most recently tried, due to lag or smthn it could be 1 or 2 attempts prior")

        time.sleep(0.5)
        screenShot(comboStr+"-on_success")
        time.sleep(1)

        if BREAK_IN_TYPE == ITEM_FRAME:
            right_click() # closes the item frame since it stays open by default (i think doors can also be set to stay open but idk/idc)

        time.sleep(3)

        # used to restart bruteforcing and count down from the value we got but that was necessary due to lag caused by the high speed, now that theres a rate limit we shouldnt need that
        
        if LEAVE_ON_SUCCESS:
            leave(inGui=(BREAK_IN_TYPE==BRIEFCASE or BREAK_IN_TYPE==CHEST))
            screenShot(comboStr+"-after_leaving")


    else:
        print(f"failed at combination {comboStr}")
        exit()





# converts the numbers used to represent the currentCombo into the characters assign to them in character_list
def comboToString(comboArray, character_list):
    combo = ""
    for val in comboArray:
        combo += character_list[val]
    return combo



# callback: a function which will be called once for each perumtation and have the permutation passed to it as an array of indices in the character_list, it will also be passed character_list. it will be also be passed the largest index from the end which was carried over ie. will pass 1 if it was 19->20. returns true if it is the correct combo and the function should return, if not returns false
# startingValues: starting array
# maxlen: the max size combination that should be iterated over
# exitCondition: a function which returns a boolean representing whether the loop should be exited
# character_list: list of characters which should be iterated over
# returns: bool, int[]. returns true if the callback returns true, returns false if does not. returns the combo at which either occured 
def iterate(callback=None, startingValues=[0], maxlen=20, exitCondition=None, character_list=DEFAULT_CHAR_LIST):

    max_value = len(character_list)-1
    currentCombo = startingValues

    print(f"iterating from {comboToString(startingValues, character_list)} to {character_list[-1] * maxlen}")

    # printing a basic calculation of how many combos there are, probably a simpler way but idc
    possibleCombos = 0
    for i in range(len(startingValues),maxlen+1):
        possibleCombos += len(character_list)**i
    print(f"~{possibleCombos} possible combinations")

    # checking the default value since the loop will increment it before checking
    if callback and callback(currentCombo, character_list, 0):
        return True, currentCombo

    while True:
        if isPressed("q") == True:
            print("paused")
            input("press enter")
            print("press q for 1 second to unpause")
            while isPressed("q") == False:
                time.sleep(1)
            print("unpaused")
            time.sleep(3)


        if (exitCondition and exitCondition()):
            return False, currentCombo

        i = len(currentCombo)-1

        # cycles through the values until it finds one that is not at its max
        # in 1249999 that would be the 4
        # in 17 that would be 7
        while currentCombo[i] == max_value:

            # if the array has reached the max value at the current length
            if i == 0:
            # adds an arbitrary value onto the end (it will get set to 0 in the next while loop)
                currentCombo.append(character_list[0])
                
                if len(currentCombo) > maxlen:
                    print("reached max length")
                    return False, currentCombo

            i-=1
        # increases the value in front of the maxed values by one
        # from 1249999 to 1259999
        # doesnt do anything if the first value was maxed cause then it would be ' '999 and an element would have already been added to the list which would server the purpose of incrementing it
        if i != -1:
            currentCombo[i]+=1
        # moves the selected value from 12'5'9999 to 125'9'999
        i+=1
        largestCarryOverPos = len(currentCombo)-i
        # sets all values from the selected one to the end to 0: 125'9'999 to 125000'0'
        while i != len(currentCombo):
            currentCombo[i] = 0
            i+=1

        if callback and callback(currentCombo, character_list, largestCarryOverPos):
            return True, currentCombo
        # time.sleep(0.1)


prevTime = 0
juststarted = True


def checkExitKey():
    return isPressed("space") or isPressed("esc")


def awaitCooldown():
    global prevTime


    changeInTime = time.time() - prevTime
    if prevTime == 0:
        changeInTime = 0
    
    time.sleep(max((PASSCODE_COOLDOWN + ADDITIONAL_DELAY) - changeInTime, 0)) # waiting for the cooldown after entering the passcode to account for the delay between entering the passcode and the chest opening
    if DEBUG: print("attempt time:", round(time.time() - prevTime, 4))
    prevTime = time.time()




def chestCallback(combo, character_list, largestCarryOverPos):
    global juststarted
    
    comboStr = comboToString(combo, character_list)

    print(comboStr)

    pyautogui.write(comboStr, interval=0.01) # could probably set interval to 0 (which it is by default) but i just want to be safe
    
    # for some reason if the first time i press enter is with the 'keyboard' library then the press doesnt register, but the pyautogui button press is much slower so i dont want to use it as the main one
    if not juststarted and OPTIMIZE_KEY_PRESSES:
        fastpress("enter")
    else:
        press("enter")
        juststarted = False

    awaitCooldown()

    # this is here so that every 100 combos it checks if it should leave because my ops are likely to be on
    # idk why i need to set largestCarryOverPos to 3 here to get it to check every 100 passcodes but with the briefcase i set it to 2 to get the same thing idrc tbh tho
    if largestCarryOverPos==3: leaveIfInBlacklistedTime(comboStr)

    # checking if the passcode was successful
    if pyautogui.pixel(TOP_RIGHT_OF_CHEST_INPUT[0],TOP_RIGHT_OF_CHEST_INPUT[1])[0] != 0:
        return True
    return False


def fastBriefcaseCallback(combo, character_list, largestCarryOverPos):

    for i in range(largestCarryOverPos+1):
        left_click(BRIEFCASE_ARROWS[3-i][0],BRIEFCASE_ARROWS[3-i][1])
    left_click(BRIEFCASE_ENTER[0], BRIEFCASE_ENTER[1])


    comboStr = comboToString(combo, character_list)
    print(comboStr)


    awaitCooldown()


    if largestCarryOverPos==2: leaveIfInBlacklistedTime(comboStr)


    # checking if the passcode was successful
    if pyautogui.pixel(BRIEFCASE_CHECK_POS[0],BRIEFCASE_CHECK_POS[1])[0] != 0:
        return True
    return False


def slowBriefcaseCallback(combo, character_list, largestCarryOverPos):
    global juststarted

    if not juststarted and OPTIMIZE_KEY_PRESSES:
        pressFunction = fastpress
    else:
        pressFunction = press
        juststarted = False



    comboStr = comboToString(combo, character_list)
    print(comboStr)

    # selecting all values that are at 9 and changing them to 0
    for _ in range(largestCarryOverPos):
        pressFunction("enter")
        pyautogui.keyDown('shift')
        pressFunction("tab")
        pressFunction("tab")
        pyautogui.keyUp('shift')
    # incrementing the first value that isnt at 9; 001'6' or 0'1'99
    pressFunction("enter")
    # moving back to the first up arrow
    for _ in range(largestCarryOverPos):
        # attempting to optimize the keybinds so it will max out the rate limit
        pressFunction("tab")
        pressFunction("tab")

    # moving from the first up arrow to the enter passcode button, clicking it, then moving back
    pressFunction("tab")
    pressFunction("tab")
    pressFunction("enter")
    pyautogui.keyDown('shift')
    pressFunction("tab")
    pressFunction("tab")
    pyautogui.keyUp('shift')

    awaitCooldown()

    if largestCarryOverPos==2: leaveIfInBlacklistedTime(comboStr)

    # checking if the passcode was successful
    if pyautogui.pixel(BRIEFCASE_CHECK_POS[0],BRIEFCASE_CHECK_POS[1])[0] != 0:
        return True
    return False


def leaveIfInBlacklistedTime(comboStr):

    # this is here so that every 100 combos it checks if it should leave because my ops are likely to be on
    if check_blacklisted_times():

        # passing true since we will always be in a gui since we havent cracked the code yet
        leave(inGui=True)
        screenShot(comboStr+"-blacklisted_time")

        print(time.asctime())
        exit(f"left because your are in a blacklisted time. last code entered: {comboStr}")



def check_blacklisted_times():
    # did have 14 (2pm) but temp removed, 5, 10
    hour = list(time.localtime())[3]
    if DEBUG: print("hour:", hour)

    return hour in BLACKLISTED_TIMES


# returns a bool of whether or not we left the game
def leave(inGui):
# this just disconnects
    if inGui:
        time.sleep(1)
        press("esc")
    time.sleep(1)
    press("esc")
    time.sleep(1)
    left_click(DISCONNECT_BUTTON[0], DISCONNECT_BUTTON[1])
    time.sleep(4)



def screenShot(name):
    ss = pyautogui.screenshot()
    
    ss.save("./images/"+name+'.png')




breakIn()