
# these are the values you may want to change, the rest should only be changed if the script is not working

LEAVE_ON_SUCCESS = True

# a list of times which if reached you want the script to stop bruteforcing and leave the game
# i used this to avoid the times at which admins would log onto the server so that i can leave before they log on to avoid unnessisary attention
# to use just add the hour which you want to leave to the list, eg. to leave at 5pm add 17 to the list
BLACKLISTED_TIMES=[]






PASSCODE_COOLDOWN = 0.250 # default value in the server config for passcode_check_cooldown is 0.250
ADDITIONAL_DELAY  = 0.08 # a value to account for lag and stuff, it should be increased if you get too many rate limit messages

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