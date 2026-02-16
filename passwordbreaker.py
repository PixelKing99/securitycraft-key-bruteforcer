import pyautogui
import time
import utils
import getCoordinates as coords

# these are the values you may want to change, the rest should only be changed if the script is not working

LEAVE_ON_SUCCESS = True

# a list of times which if reached you want the script to stop bruteforcing and leave the game
# i used this to avoid the times at which admins would log onto the server so that i can leave before they log on to avoid unnessisary attention
# to use just add the hour which you want to leave to the list, eg. to leave at 5pm add 17 to the list
BLACKLISTED_TIMES=[]






PASSCODE_COOLDOWN = 0.250 # default value in the server config for passcode_check_cooldown is 0.250

# basically makes it so that on the first passcode entry it uses the default slow keypress method and then subsequently uses the fast method since for some reason that works
# if keypresses are failing to register then you should turn this off maybe, but then pressing buttons will be slower
OPTIMIZE_KEY_PRESSES = True

# uses the mouse to press the arrows instead of using the tab keys to navigate due to the fact that making sure the tab presses register is quite slow
USE_FAST_BRIEFCASE_MODE = True

DEBUG = False # outputting additional information

# 'enum' of bruteforce types
CHEST = 0
BRIEFCASE = 1
ITEM_FRAME = 2
DOOR = 3




# default
DEFAULT_CHAR_LIST = ["0","1","2","3","4","5","6","7","8","9"]

# from my 'testing' here is the count of times each number was the first digit
# having a + means the second number is the number of times it was used exclusively as a briefcase password,
# which is significant cause you cant type briefcase passcodes and instead have to use arrows to increment the values
# so some will be easier to type than others, making the passcode potentially biased towards easy to type combos
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
# based off this data here is the 'technically' most optimized order with the priority being number of time used for a regular passcode and uses for passcodes being a tiebreaker
OPTIMIZED_CHAR_LIST = ["1","2","0","5","4","6","8","3","7","9"]



BREAK_IN_TYPE = int(input(f"enter the number corrospoding to what you are bruteforcing:\n{CHEST}. chest\n{BRIEFCASE}. briefcase\n{ITEM_FRAME}. item frame\n{DOOR}. door\n"))

if BREAK_IN_TYPE in [CHEST, BRIEFCASE, ITEM_FRAME, DOOR]:
    if BREAK_IN_TYPE == BRIEFCASE:
        additional_delay = 0.18 # i had it as the same value but then only briefcases were getting the rate limit message so ig we'll just have it as 2 different messages
    else:
        additional_delay = 0.08
else:
    exit("invalid option")

ADDITIONAL_DELAY = additional_delay


DISCONNECT_BUTTON, TOP_RIGHT_OF_CHEST_INPUT, SHOW_PASSCODE, BRIEFCASE_CHECK_POS, BRIEFCASE_DOWN_ARROW, BRIEFCASE_ARROWS, BRIEFCASE_ENTER = coords.getPositions(BREAK_IN_TYPE)

print("press 'space' or 'esc' to stop bruteforcing or 'q' to pause")
print("starting in 5")
time.sleep(5)



def breakIn():
    if BREAK_IN_TYPE == CHEST or BREAK_IN_TYPE == ITEM_FRAME or BREAK_IN_TYPE == DOOR:
        
        utils.left_click(SHOW_PASSCODE[0], SHOW_PASSCODE[1])
        time.sleep(0.1)
        utils.left_click(TOP_RIGHT_OF_CHEST_INPUT[0], TOP_RIGHT_OF_CHEST_INPUT[1])

        CHAR_LIST = OPTIMIZED_CHAR_LIST

        success, combo = iterate(callback=chestCallback, character_list=CHAR_LIST, maxlen=5)
        comboStr = utils.comboToString(combo, CHAR_LIST)


    elif BREAK_IN_TYPE == BRIEFCASE:
        if USE_FAST_BRIEFCASE_MODE == True:
            
            utils.left_click(BRIEFCASE_DOWN_ARROW[0], BRIEFCASE_DOWN_ARROW[1])
            currentCallback = fastBriefcaseCallback
            pass
        else:

            # this sets up the briefcase so that we can use tab and shift+tab to navigate the arrows
            utils.left_click(BRIEFCASE_DOWN_ARROW[0], BRIEFCASE_DOWN_ARROW[1])
            pyautogui.keyDown("shift")
            pyautogui.press("tab")
            pyautogui.keyUp("shift")
            currentCallback = slowBriefcaseCallback


        # i need to make sure i dont set the character list to anything other than the default cause i cant change the order i enter the numbers in with the briefcase
        success, combo = iterate(startingValues=[0,0,0,0], maxlen=4, callback=currentCallback)
        comboStr = utils.comboToString(combo, DEFAULT_CHAR_LIST)
    
    
    
    if success:

        print("the passcode should be one of the ones which was most recently tried, due to lag or smthn it could be 1 or 2 attempts prior")

        time.sleep(0.5)
        utils.screenShot(comboStr+"-on_success")
        time.sleep(1)

        if BREAK_IN_TYPE == ITEM_FRAME:
            utils.right_click() # closes the item frame since it stays open by default (i think doors can also be set to stay open but idk/idc)

        time.sleep(3)

        # used to restart bruteforcing and count down from the value we got but that was necessary due to lag caused by the high speed, now that theres a rate limit we shouldnt need that
        
        if LEAVE_ON_SUCCESS:
            leave(inGui=(BREAK_IN_TYPE==BRIEFCASE or BREAK_IN_TYPE==CHEST))
            utils.screenShot(comboStr+"-after_leaving")


    else:
        print(f"failed at combination {comboStr}")
        exit()




# callback: a function which will be called once for each perumtation 
#   int[]: it will have the permutation passed to it as an array of indices in the character_list,
#   string[]: it will also be passed character_list.
#   int: it will be also be passed the largest index from the end which was carried over ie. will pass 1 if it was 19->20.
#   return: it should return true if it is the correct combo, if not returns false
# int[] startingValues: starting array
# int maxlen: the max size combination that should be iterated over
# string[] character_list: list of characters which should be iterated over
# returns: bool, int[]. returns true if the callback returns true, returns false if does not. returns the combo at which either occured 
def iterate(callback=None, startingValues=[0], maxlen=20, character_list=DEFAULT_CHAR_LIST):

    max_value = len(character_list)-1
    currentCombo = startingValues

    print(f"iterating from {utils.comboToString(startingValues, character_list)} to {character_list[-1] * maxlen}")

    # printing a basic calculation of how many combos there are, probably a simpler way but idc
    possibleCombos = 0
    for i in range(len(startingValues),maxlen+1):
        possibleCombos += len(character_list)**i
    print(f"~{possibleCombos} possible combinations")

    # checking the default value since the loop will increment it before checking
    if callback and callback(currentCombo, character_list, 0):
        return True, currentCombo

    while True:
        if utils.isPressed("q") == True:
            print("paused")
            input("press enter")
            print("press q for 1 second to unpause")
            while utils.isPressed("q") == False:
                time.sleep(1)
            print("unpaused")
            time.sleep(3)


        if utils.checkExitKey():
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






juststarted = True



def chestCallback(combo, character_list, largestCarryOverPos):
    global juststarted
    
    comboStr = utils.comboToString(combo, character_list)

    print(comboStr)

    pyautogui.write(comboStr, interval=0.01) # could probably set interval to 0 (which it is by default) but i just want to be safe
    
    # for some reason if the first time i press enter is with the 'keyboard' library then the press doesnt register
    # but the pyautogui button press is much slower so i dont want to use it as the main one
    if not juststarted and OPTIMIZE_KEY_PRESSES:
        utils.fastpress("enter")
    else:
        utils.press("enter")
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
        utils.left_click(BRIEFCASE_ARROWS[3-i][0],BRIEFCASE_ARROWS[3-i][1])
    utils.left_click(BRIEFCASE_ENTER[0], BRIEFCASE_ENTER[1])


    comboStr = utils.comboToString(combo, character_list)
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
        pressFunction = utils.fastpress
    else:
        pressFunction = utils.press
        juststarted = False



    comboStr = utils.comboToString(combo, character_list)
    print(comboStr)

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
    pressFunction("enter")
    pyautogui.keyDown("shift")
    pressFunction("tab")
    pressFunction("tab")
    pyautogui.keyUp("shift")

    awaitCooldown()

    if largestCarryOverPos==2: leaveIfInBlacklistedTime(comboStr)

    # checking if the passcode was successful
    if pyautogui.pixel(BRIEFCASE_CHECK_POS[0],BRIEFCASE_CHECK_POS[1])[0] != 0:
        return True
    return False


# returns a bool of whether or not we left the game
def leave(inGui):
# this just disconnects
    if inGui:
        time.sleep(1)
        utils.press("esc")
    time.sleep(1)
    utils.press("esc")
    time.sleep(1)
    utils.left_click(DISCONNECT_BUTTON[0], DISCONNECT_BUTTON[1])
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
    if check_blacklisted_times():

        # passing true since we will always be in a gui since we havent cracked the code yet
        leave(inGui=True)
        utils.screenShot(comboStr+"-blacklisted_time")

        print(time.asctime())
        exit(f"left because your are in a blacklisted time. last code entered: {comboStr}")



def check_blacklisted_times():
    # did have 14 (2pm) but temp removed, 5, 10
    hour = list(time.localtime())[3]
    if DEBUG: print("hour:", hour)

    return hour in BLACKLISTED_TIMES




breakIn()