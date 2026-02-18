import pyautogui
import time
import util
import getCoordinates as coords
from iterate import iterate

from consts import *

print("btw you may want to empty your hotbar before starting bc after opening the inventory it may press some numbers before realizing its open which will move your items around")
BREAK_IN_TYPE = int(input(f"enter the number corrospoding to what you are bruteforcing:\n{CHEST}. chest\n{BRIEFCASE}. briefcase\n{ITEM_FRAME}. item frame\n{DOOR}. door\n"))

if BREAK_IN_TYPE not in [CHEST, BRIEFCASE, ITEM_FRAME, DOOR]:
    exit("invalid option")


DISCONNECT_BUTTON, TOP_RIGHT_OF_CHEST_INPUT, SHOW_PASSCODE, BRIEFCASE_CHECK_POS, BRIEFCASE_DOWN_ARROW, BRIEFCASE_ARROWS, BRIEFCASE_ENTER = coords.getPositions(BREAK_IN_TYPE)

print("press 'space', 's', or 'esc' to stop bruteforcing or 'q' to pause")
print("starting in 5")
time.sleep(5)



def breakIn():
    if BREAK_IN_TYPE == CHEST or BREAK_IN_TYPE == ITEM_FRAME or BREAK_IN_TYPE == DOOR:
        
        util.left_click(SHOW_PASSCODE)
        time.sleep(0.1)
        util.left_click(TOP_RIGHT_OF_CHEST_INPUT)

        CHAR_LIST = OPTIMIZED_CHAR_LIST

        success, combo = iterate(callback=chestCallback, character_list=CHAR_LIST, maxlen=5)
        comboStr = util.comboToString(combo, CHAR_LIST)


    elif BREAK_IN_TYPE == BRIEFCASE:
        if USE_FAST_BRIEFCASE_MODE == True:
            
            # this sets it essentially to -1 so that when it is called for the first time it increments it and checks 0,0,0,0
            util.left_click(BRIEFCASE_DOWN_ARROW)
            
            currentCallback = fastBriefcaseCallback
        else:

            # this sets up the briefcase so that we can use tab and shift+tab to navigate the arrows
            util.left_click(BRIEFCASE_DOWN_ARROW)
            pyautogui.keyDown("shift")
            pyautogui.press("tab")
            pyautogui.keyUp("shift")
            currentCallback = slowBriefcaseCallback


        # i need to make sure i dont set the character list to anything other than the default cause i cant change the order i enter the numbers in with the briefcase
        success, combo = iterate(startingValues=[0,0,0,0], maxlen=4, callback=currentCallback)
        comboStr = util.comboToString(combo, DEFAULT_CHAR_LIST)
    
    
    
    if success:

        print("the passcode should be one of the ones which was most recently tried, due to lag or smthn it could be 1 or 2 attempts prior")

        time.sleep(0.5)
        util.screenShot(comboStr+"-on_success")
        time.sleep(1)



        # used to restart bruteforcing and count down from the value we got but that was necessary due to lag caused by the high speed, now that theres a rate limit we shouldnt need that
        
        if LEAVE_ON_SUCCESS:
            if BREAK_IN_TYPE == ITEM_FRAME:
                util.right_click() # closes the item frame since it stays open by default (i think doors can also be set to stay open but idk/idc)
                time.sleep(1)


            leave(inGui=(BREAK_IN_TYPE==BRIEFCASE or BREAK_IN_TYPE==CHEST))
            util.screenShot(comboStr+"-after_leaving")


    else:
        print(f"failed at combination {comboStr}")
        exit()




juststarted = True



def chestCallback(comboStr, largestCarryOverPos):
    global juststarted

    pyautogui.write(comboStr, interval=0.01) # could probably set interval to 0 (which it is by default) but i just want to be safe
    
    
    awaitCooldown()
    
    # for some reason if the first time i press enter is with the 'keyboard' library then the press doesnt register
    # but the pyautogui button press is much slower so i dont want to use it as the main one
    if not juststarted and OPTIMIZE_KEY_PRESSES:
        util.fastpress("enter")
    else:
        util.press("enter")
        juststarted = False


    # this is here so that every 100 combos it checks if it should leave because my ops are likely to be on
    if largestCarryOverPos>=2: leaveIfInBlacklistedTime(comboStr)

    # checking if the passcode was successful
    if pyautogui.pixel(TOP_RIGHT_OF_CHEST_INPUT[0],TOP_RIGHT_OF_CHEST_INPUT[1])[0] != 0:
        return True
    return False






def fastBriefcaseCallback(comboStr, largestCarryOverPos):

    for i in range(largestCarryOverPos+1):
        util.left_click(BRIEFCASE_ARROWS[3-i])


    awaitCooldown()

    # pressing enter after the cooldown should help to ensure that the time between each attempt is equal but it also will make the success check more delayed (more attemps could occur before it realizes the invetory is open)
    util.left_click(BRIEFCASE_ENTER)

    if largestCarryOverPos>=2: leaveIfInBlacklistedTime(comboStr)


    # checking if the passcode was successful
    if pyautogui.pixel(BRIEFCASE_CHECK_POS[0],BRIEFCASE_CHECK_POS[1])[0] != 0:
        return True
    return False




def slowBriefcaseCallback(comboStr, largestCarryOverPos):
    global juststarted

    if not juststarted and OPTIMIZE_KEY_PRESSES:
        pressFunction = util.fastpress
    else:
        pressFunction = util.press
        juststarted = False

    # selecting all values that are at 9 and changing them to 0
    for _ in range(largestCarryOverPos):
        pressFunction("enter")
        pyautogui.keyDown("shift")
        pressFunction("tab")
        pressFunction("tab")
        pyautogui.keyUp("shift")
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


    awaitCooldown()
    
    
    pressFunction("enter")
    pyautogui.keyDown("shift")
    pressFunction("tab")
    pressFunction("tab")
    pyautogui.keyUp("shift")


    if largestCarryOverPos>=2: leaveIfInBlacklistedTime(comboStr)

    # checking if the passcode was successful
    if pyautogui.pixel(BRIEFCASE_CHECK_POS[0],BRIEFCASE_CHECK_POS[1])[0] != 0:
        return True
    return False


# returns a bool of whether or not we left the game
def leave(inGui):
# this just disconnects
    if inGui:
        time.sleep(1)
        util.press("esc")
    time.sleep(1)
    util.press("esc")
    time.sleep(1)
    util.left_click(DISCONNECT_BUTTON)
    time.sleep(4)



prevTime = time.time()

def awaitCooldown():
    global prevTime


    changeInTime = time.time() - prevTime
    if prevTime == 0:
        changeInTime = 0
    
    time.sleep(max((PASSCODE_COOLDOWN + ADDITIONAL_DELAY) - changeInTime, 0)) # waiting for the cooldown after entering the passcode to account for the delay between entering the passcode and the chest opening
    if DEBUG: print("attempt time:", round(time.time() - prevTime, 4))
    
    additionalTime = round((time.time() - prevTime) - (PASSCODE_COOLDOWN + ADDITIONAL_DELAY), 3)
    if additionalTime > 0: print(f"attempt took {additionalTime}s longer than desired")

    prevTime = time.time()


def leaveIfInBlacklistedTime(comboStr):

    # this is here so that every 100 combos it checks if it should leave because my ops are likely to be on
    if util.check_blacklisted_times():

        # passing true since we will always be in a gui since we havent cracked the code yet
        leave(inGui=True)
        util.screenShot(comboStr+"-blacklisted_time")

        print(time.asctime())
        exit(f"left because your are in a blacklisted time. last code entered: {comboStr}")




breakIn()