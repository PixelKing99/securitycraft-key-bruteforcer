import util
import time
from consts import *


# callback: a function which will be called once for each perumtation 
#   string: the string representation of the current combo
#   int: it will be also be passed the largest index from the end which was carried over ie. will pass 1 if it was 19->20.
#   return: it should return true if it is the correct combo, if not false
# int[] startingValues: starting array
# int maxlen: the max size combination that should be iterated over
# string[] character_list: list of characters which should be iterated over
# returns: bool, int[]. returns true if the callback returns true, returns false if does not. returns the combo at which either occured 
def iterate(callback=None, startingValues=[0], maxlen=20, character_list=DEFAULT_CHAR_LIST):

    max_value = len(character_list)-1
    currentCombo = startingValues

    # checking the default value since the loop will increment it before checking
    if callback and callback(util.comboToString(currentCombo, character_list), 0):
        return True, currentCombo

    while True:
        if util.isPressed("q") == True:
            print("paused")
            input("press enter")
            print("press q for 1 second to unpause")
            while util.isPressed("q") == False:
                time.sleep(1)
            print("unpaused")
            time.sleep(3)


        if util.checkExitKey():
            return False, currentCombo

        i = len(currentCombo)-1

        # this value is used to give the callback function the most significant digit change, in 17->18 that would be the 7 whos position would be represented as 0
        # we are currently setting to the length which would represent the value before the start of the number
        # we are doing this here so that if the length of the current combo changes (upon reaching the max value) it will not cause it to be messed up type shi, idk
        largestCarryOverPos = len(currentCombo)

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
        # doesnt do anything if the first value was maxed cause then it would be ' '999 and an element would have already been added to the list which would serve the purpose of incrementing it
        if i != -1:
            currentCombo[i]+=1
        # moves the selected value from 12'5'9999 to 125'9'999
        i+=1

        # updates the carry over position and stuff, idk
        largestCarryOverPos -= i

        # sets all values from the selected one to the end to 0: 125'9'999 to 125000'0'
        while i != len(currentCombo):
            currentCombo[i] = 0
            i+=1

        comboStr = util.comboToString(currentCombo, character_list)
        print(comboStr)

        if callback and callback(comboStr, largestCarryOverPos):
            return True, currentCombo