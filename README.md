this is a macro that will bruteforce the passcodes of various blocks and items from the securitycraft mod for minecraft, it was intended to only be used by me so its not very good

the devs added a cooldown to entering passcodes so this is far less useful however its still somewhat practical for briefcases and can crack them in an hour or so i think

tbh it is kinda dumb to use a macro for this and a mod would be better suited for this but as i said this was only really intended for personal use

# disclaimer
it aint my problem what you do with this


# how to use

## linux
this is for debian based linux that i use, if it doesnt work for you, idrc you can probably figure it out yourself


to install the requirements for the script you will want to run these commands while in the repository directory:
```
python -m venv ./env
source env/bin/activate
pip install -r requirements.txt
```

you need to be root to run the script cause pyautogui requires it, to do this you will probably want to run these commands:
```
sudo su
source env/bin/activate
```

to run the script just run passwordbreaker with python and then follow the prompts that appear in the terminal:
```
python passwordbreaker.py
```

## windows:
to install the requirements for the script you will want to run these commands while in the repository directory:
```
python -m venv env
env\Scripts\activate.bat
pip install -r requirements.txt
```

when running subsequent times, make sure you are in the virtual environment:
```
env\Scripts\activate.bat
```

to run the script just run passwordbreaker with python and then follow the prompts that appear in the terminal:
```
python passwordbreaker.py
```