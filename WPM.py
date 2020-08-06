import os
import tkinter as tk
from datetime import datetime
from time import sleep


class configuration():

    def __init__(self):
        self.FontSize = 0
        self.WPM = 0
        try:
            config = open("default.cfg", "r")
            if config:
                self.FontSize = config.readline()[-3:-1]
                self.WPM = config.readline()[-3:-1]
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            print("Generating default config...")
            sleep(1)
            file = open("default.cfg", "w")
            defaults = ["FontSize=50\n", "WordsPerMinute=30"]
            file.writelines(defaults)
            file.close()
        finally:
            print("Words Per Minute!\n")
            print("0. Use Default Config?")
            print("1. Make Custom Config?")
            choice = int(input("Enter Choice (0/1): "))
            if not choice:
                config = open("default.cfg", "r")
                self.FontSize = config.readline()[-3:-1]
                self.WPM = config.readline()[-3:-1]
                config.close()
            else:
                self.FontSize, self.WPM = self.UserConfiguration()

        try:
            para = open("para.txt", "r")
            if not para:
                raise FileNotFoundError
            else:
                choice = 0
                choice = int(
                    input("\n0. Use existing para?\n1. Make new para? \nEnter choice: "))
                if choice:
                    raise FileNotFoundError
                else:
                    para.close()
        except FileNotFoundError:
            para = open("para.txt", "w")
            os.startfile("para.txt")
            print("Write your words in para.txt\n\n")
            para.close()
        print("Use <Escape>, <F11> to manipulate the window's fullscreen properties!\n")

    def UserConfiguration(self):

        now = datetime.now()
        # datetime object containing current date and time

        # dd_mm_YY__H_M_S
        dt_string = now.strftime("%d_%m_%Y__%H_%M_%S")
        self.FontSize = int(input("Enter Font size: "))
        self.WPM = int(input("Enter Words per Minute: "))
        usrCFGfile = str("config_" + dt_string + ".cfg")
        userconfig = open(usrCFGfile, "w")
        userconfig.writelines("FontSize=" + str(self.FontSize))
        userconfig.writelines("\nWordsPerMinute=" + str(self.WPM))
        print("User config saved in " + usrCFGfile)
        userconfig.close()
        return (self.FontSize, self.WPM)

    def GetFontSize(self):
        return int(self.FontSize)

    def getWPM(self):
        return int(self.WPM)


# This code snippet now flashes the words per minute.

cofg = configuration()
para = open("para.txt", "r")
words = [str(x) for x in para.read().split()]


def Miliseconds_per_word():
    return 60000 / cofg.getWPM()


MPW = Miliseconds_per_word()

root = tk.Tk()
root.attributes("-fullscreen", True)
root.bind("<F11>", lambda event: root.attributes("-fullscreen", not root.attributes("-fullscreen")))
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))
root.bind("<F1>", lambda event: os.exit(0))

w = tk.StringVar()

labelFlash = tk.Label(root, bg='Black', width=root.winfo_screenwidth(), height=root.winfo_screenheight(),
                      anchor="center", text="Sample", fg="White", font="Times " + str(cofg.GetFontSize()), textvariable=w)
labelFlash.pack()
indx = 0


def update():
    global indx
    if indx >= len(words):
        indx = 0
    w.set(words[indx])
    labelFlash.config(text=words[indx])
    indx += 1
    root.after(int(MPW), update)


update()
root.mainloop()
