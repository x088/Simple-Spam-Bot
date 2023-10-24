print("loading...")
import sys
from os.path import isfile
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import ThemedTk
import pyautogui
import threading
import time
import json

# loading settings and some global variables

# Colors

bgc = "#333"
abgc = "#222"
fgc = "#ddd"
afgc = "#333"

disableSettings = False # this is set to True when the settings file is not found to disable the settings tab
global spamming
spamming = True # This is set to False when the stop button is pressed to stop the spamming functions, this 
# is not the most efficient way to do this but multithreading makes it much harder for me to figure out a better way to do it

try:

    importSettings = open('settings.json', 'r')
    settingsF = json.load(importSettings)

except FileNotFoundError as error:

    print("\nError: Could not find the Settings file (settings.json)")
    print("The default settings will be used and the Settings tab will be disabled until the settings file is retrieved/replaced")
    print("Error message:\n   ", "FileNotFoundError: {0}".format(error))
    disableSettings = True
    startingDelay = float("5")
    messageDelay = float("0.2")
    textEnding = "enter"

except:

    print("\nError: An unexpected error occured while importing the settings from the settings file (settings.json), \nPlease send this error message to the developer to try to fix this issue.")
    print("Error message: ")
    raise

else:

    try:
        startingDelay = float(settingsF["startingDelay"])
    except ValueError as sdverr:
        startingDelay = float("5")
        print("\nError: The starting delay is either not found or not set to a valid number, the bot will use the default \nstarting delay until you change it from the settings tab")
        print("NOTE: The settings tab might show a different value than the actual value that caused this error")
        print("Error message: ", "ValueError: {0}".format(sdverr))

    except KeyError as sdkerr:

        startingDelay = float("5")
        print("\nError: The starting delay is either not found or not set to a valid number, the bot will use the default \nstarting delay until you change it from the settings tab")
        print("NOTE: The settings tab might show a different value than the actual value that caused this error")
        print("Error message: ", "KeyError: {0}".format(sdkerr))

    try:
        messageDelay = float(settingsF["messageDelay"])
    except ValueError as mdverr:

        messageDelay = float("0.2")
        print("\nError: The message delay is either not found or not set to a valid number, the bot will use the default \nstarting delay until you change it from the settings tab")
        print("NOTE: The settings tab might show a different value than the actual value that caused this error")
        print("Error message: ", "ValueError: {0}".format(mdverr))

    except KeyError as mdkerr:

        messageDelay = float("0.2")
        print("\nError: The message delay is either not found or not set to a valid number, the bot will use the default \nstarting delay until you change it from the settings tab")
        print("NOTE: The settings tab might show a different value than the actual value that caused this error")
        print("Error message: ", "KeyError: {0}".format(mdkerr))

    try:
        textEnding = settingsF["textEnding"]
    except KeyError as tekerr:

        textEnding = "enter"
        print("\nError: The text ending is either not found or not set to a valid value, the bot will use the default \nstarting delay until you change it from the settings tab")
        print("A list of valid keys can be found here: https://pytutorial.com/pyautogui-keyboard-keys")
        print("NOTE: The settings tab might show a different value than the actual value that caused this error")
        print("Error message: ", "KeyError: {0}".format(tekerr))
        
# Functions

def textSpam():

    global spamming
    startTSB.config(state="disabled") # don't forget to disable the start button to not cause performance issues and
    # unwanted behaviour if the user was impatient and pressed the start button more that one time
    text = str(textTSE.get())
    number = numberTSE.get()
    try:
        number = int(number)
    except ValueError as error:
        print("Error: You can only type numbers here not letters")
        print("Error message:\n   ", "ValueError: {0}".format(error))
        spamming = False
        startTSB.config(state="normal") # re-enable the start button if an error 
        # occured so the user doesn't have to restart the app to be able to start again
        sys.exit()

    startingNumber = 0
    messagesSpammed = 0

    time.sleep(startingDelay)

    if spamming is True:
        print("Started Spamming")
        while startingNumber < number:
            if spamming is False:
                sys.exit()

            pyautogui.typewrite(text)
            pyautogui.press(textEnding)
            time.sleep(messageDelay)

            startingNumber += 1
            messagesSpammed += 1
            messagesLeft = number - messagesSpammed

            messagesSpammedTSL.configure(text=f"Messages spammed: {messagesSpammed}")
            messagesLeftTSL.configure(text=f"Messages left: {messagesLeft}")
        
    print("Done!")    
    startTSB.config(state="normal") # also don't forget to enable the start button again when the spamming ends
    sys.exit()

def infiniteSpam():
        
    global enableStartISV
    enableStartISV = True

    startISB.config(state="disabled")

    text = str(textISE.get())

    messagesSpammed = 0
    time.sleep(startingDelay)
    print("Started Spamming")
    
    while True:
        if enableStartISV:
            if spamming is False:
                sys.exit()

            pyautogui.typewrite(text)
            pyautogui.press(textEnding)
            time.sleep(messageDelay)

            messagesSpammed += 1
            messagesSpammedISL.configure(text=f"Messages spammed: {messagesSpammed}")
        else:
            startISB.config(state="normal")
            sys.exit()
            

def uploadFile(event=None):

    textfile = filedialog.askopenfilename()
    filePath.set(textfile)
    print(f"Selected file: {textfile}")

def fileSpam():

    global spamming
        
    try:
        path = pathFSE.get()
        f = open(path,'r')
    except FileNotFoundError as fnferr:
        print("\nError: That file doesn't exist, make sure you've typed the correct file name/path")
        print("Error message: ", "FileNotFoundError: {0}".format(fnferr))
        spamming = False
        startFSB.config(state="normal")

    time.sleep(startingDelay)
    messagesSpammed = 0
    spamming = True

    print("Started Spamming")
    for word in f:
        if spamming is False:
            break
        else:
            pyautogui.typewrite(word)
            pyautogui.press(textEnding)
            time.sleep(messageDelay)

            messagesSpammed += 1
            messagesSpammedFSL.configure(text=f"Messages spammed: {messagesSpammed}")

    print("Done!")
    startFSB.config(state="normal")
    sys.exit()

def startTS(): # for text spam mode

    global spamming
    spamming = True
    TSthread = threading.Thread(target=textSpam)
    TSthread.start()

def startIS(): # for infinite spam mode

    global spamming
    spamming = True
    ISthread = threading.Thread(target=infiniteSpam)
    ISthread.start()

def startFS(): # for file spam mode

    global spamming
    spamming = True
    FSthread = threading.Thread(target=fileSpam)
    FSthread.start()

def stop(): # stops all the spamming functions

    global spamming, enableStartISV
    enableStartISV = False
    spamming = False
    print("Stopped Spamming")

def applySettings():

    startingDelayI = startingDelaySE.get()
    messageDelayI = messageDelaySE.get()
    textEndingI = textEndingSE.get()

    settingsF["startingDelay"] = startingDelayI
    settingsF["messageDelay"] = messageDelayI
    settingsF["textEnding"] = textEndingI

    settingsFile = open("settings.json", "w")
    json.dump(settingsF, settingsFile)
    print("Saved! \nRestart to apply changes")

def resetSettings():

    settingsF["startingDelay"] = float("5")
    settingsF["messageDelay"] = float("0.2")
    settingsF["textEnding"] = "enter"

    startingDelaySV.set("5")
    messageDelaySV.set("0.2")
    textEndingSV.set("enter")

    settingsFile = open("settings.json", "w")
    json.dump(settingsF, settingsFile)
    print("Your settings are set back to default. Restart to apply changes")

# Setting up the GUI

root = ThemedTk(theme="equilux")
root.geometry("720x850")
root.resizable(0,0)
root.title("Spam bot")
root.config(background=bgc)

tabs = ttk.Notebook(root)

TSTab = Frame(tabs)
FSTab = Frame(tabs)
ISTab = Frame(tabs)
settingsT = Frame(tabs)

tabs.add(TSTab, text="Text Spam mode")
tabs.add(ISTab, text="Infinite Spam mode")
tabs.add(FSTab, text="File Spam mode")
tabs.add(settingsT, text="Settings")

tabs.pack(expand=True, fill="both")

TSTab.config(background=bgc)
ISTab.config(background=bgc)
FSTab.config(background=bgc)
settingsT.config(background=bgc)

# This if statement disables the settings tab if the settings file is not found to avoid errors

if disableSettings is True:
    tabs.tab(3, state="disabled")
else:
    tabs.tab(3, state="normal")

# more global variables

filePath = StringVar()

startingDelaySV = StringVar()
messageDelaySV = StringVar()
textEndingSV = StringVar()

startingDelaySV.set(startingDelay)
messageDelaySV.set(messageDelay)
textEndingSV.set(textEnding)

# The GUI layout code

# Text Spam (TS) mode tab

titleTSL = Label(TSTab, text="Spam Bot", bg=bgc, fg=fgc, font=("Arial", 24))
textTSL = Label(TSTab, text="Enter the text you want to spam:", bg=bgc, fg=fgc, font=("Arial", 16))
textTSE = Entry(TSTab, width=50, bg=bgc, fg=fgc, font=("Arial", 16))
numberTSL = Label(TSTab, text="How many times do you want to spam it:", bg=bgc, fg=fgc, font=("Arial", 16))
numberTSE = Entry(TSTab, width=50, bg=bgc, fg=fgc, font=("Arial", 16))
messagesSpammedTSL = Label(TSTab, text="", bg=bgc, fg=fgc, font=("Arial", 14))
messagesLeftTSL = Label(TSTab, text="", bg=bgc, fg=fgc, font=("Arial", 16))
startTSB = Button(TSTab, text="Start", bg=bgc, fg=fgc, font=("Arial", 24), activebackground=abgc, activeforeground=afgc, command=startTS)
stopTSB = Button(TSTab, text="Stop", bg=bgc, fg=fgc, font=("Arial", 24), activebackground=abgc, activeforeground=afgc, command=stop)

titleTSL.pack(padx=30, pady=20)
textTSL.pack(fill='both')
textTSE.pack(padx=10,pady=10, ipady=10)
numberTSL.pack()
numberTSE.pack(padx=10, pady=10, ipady=10)
messagesSpammedTSL.pack()
messagesLeftTSL.pack()
startTSB.pack(padx=10, pady=10)
stopTSB.pack(padx=10, pady=10)

# Infinite Spam (IS) mode tab

titleISL = Label(ISTab, text="Spam Bot", bg=bgc, fg=fgc, font=("Arial", 24))
textISL = Label(ISTab, text="Enter the text you want to spam:", bg=bgc, fg=fgc, font=("Arial", 16))
textISE = Entry(ISTab, bg=bgc, fg=fgc, font=("Arial", 16), width=50)
messagesSpammedISL = Label(ISTab, text="", bg=bgc, fg=fgc, font=("Arial", 14))
startISB = Button(ISTab, text="Start", bg=bgc, fg=fgc, activebackground=abgc, activeforeground=afgc, font=("Arial", 24), command=startIS)
stopISB = Button(ISTab, text="Stop", bg=bgc, fg=fgc, activebackground=abgc, activeforeground=afgc, font=("Arial", 24), command=stop)

titleISL.pack(padx=30, pady=20)
textISL.pack(fill='both')
textISE.pack(padx=10,pady=10, ipady=10)
messagesSpammedISL.pack()
startISB.pack(padx=10, pady=10)
stopISB.pack(padx=10, pady=10)

# File Spam (FS) mode tab

titleFSL = Label(FSTab, text="Spam Bot", bg=bgc, fg=fgc, font=("Arial", 24))
pathFSL = Label(FSTab, text="File path:", bg=bgc, fg=fgc, font=("Arial", 16))
pathFSE = Entry(FSTab, textvariable=filePath, bg=bgc, fg=fgc, font=("Arial", 16), width=50)
messagesSpammedFSL = Label(FSTab, text="", bg=bgc, fg=fgc, font=("Arial", 14))
uploadFSB = Button(FSTab, text='Select File', bg=bgc, fg=fgc, font=("Arial", 24), activebackground=abgc, activeforeground=afgc, command=uploadFile)
startFSB = Button(FSTab, text="Start", bg=bgc, fg=fgc, font=("Arial", 24), activebackground=abgc, activeforeground=afgc, command=startFS)
stopFSB = Button(FSTab, text="Stop", bg=bgc, fg=fgc, font=("Arial", 24), activebackground=abgc, activeforeground=afgc, command=stop)

titleFSL.pack(padx=30, pady=20)
pathFSL.pack(fill='both')
pathFSE.pack(padx=10,pady=10, ipady=10)
messagesSpammedFSL.pack()
uploadFSB.pack(padx=10, pady=10)
startFSB.pack(padx=10, pady=10)
stopFSB.pack(padx=10, pady=10)

# Settings (S) tab

titleSL = Label(settingsT, text="Settings", bg=bgc, fg=fgc, font=("Arial", 24))
startingDelaySL = Label(settingsT, text="Starting Delay:", anchor='w', bg=bgc, fg=fgc, font=("Arial", 16))
startingDelaySE = Entry(settingsT, textvariable=startingDelaySV, bg=bgc, fg=fgc, font=("Arial", 16), width=40)
messageDelaySL = Label(settingsT, text="Message Delay:", anchor='w', bg=bgc, fg=fgc, font=("Arial", 16))
messageDelaySE = Entry(settingsT, textvariable=messageDelaySV, bg=bgc, fg=fgc, font=("Arial", 16), width=40)
textEndingSL = Label(settingsT, text="Button pressed after each sentence:", anchor='w', bg=bgc, fg=fgc, font=("Arial", 16))
textEndingSE = Entry(settingsT, textvariable=textEndingSV, bg=bgc, fg=fgc, font=("Arial", 16), width=40)
availableKeysSL = Label(settingsT, text="list of available keys can be found here: https://pytutorial.com/pyautogui-keyboard-keys", anchor='w', bg=bgc, fg=fgc, font=("Arial", 10))
saveSB = Button(settingsT, text="Save", bg=bgc, fg=fgc, font=("Arial", 24), activebackground=abgc, activeforeground=afgc, command=applySettings)
resetSB = Button(settingsT, text="Reset to default", bg=bgc, fg=fgc, font=("Arial", 20), activebackground=abgc, activeforeground=afgc, command=resetSettings)
noteSL = Label(settingsT, text="Note: you'll have to restart the app to apply changes", bg=bgc, fg=fgc, font=("Arial", 14))

titleSL.pack(padx=30, pady=20)
startingDelaySL.pack(fill='both')
startingDelaySE.pack(padx=10,pady=10, ipady=10, side="top", anchor="e")
messageDelaySL.pack(fill='both')
messageDelaySE.pack(padx=10,pady=10, ipady=10, side="top", anchor="e")
textEndingSL.pack(fill='both')
textEndingSE.pack(padx=10,pady=10, ipady=10, side="top", anchor="e")
availableKeysSL.pack(fill='both')
saveSB.pack(padx=10, pady=10)
resetSB.pack(padx=7, pady=7)
noteSL.pack()

print("Done loading!\n")

if __name__ == '__main__':
    root.mainloop()
