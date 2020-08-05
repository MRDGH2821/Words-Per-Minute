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
                FontSize = config.readline()[-2:]
                WPM = config.readline()[-2:]
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
                FontSize = config.readline()[-2:]
                WPM = config.readline()[-2:]
                config.close()
            else:
                FontSize, WPM = self.UserConfiguration()

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
        print("Use <F11> to enter into Fullscreen, <Esc> to exit fullscreen, <F1> to exit; in the new window created in background\n ")

    def UserConfiguration(self):

        now = datetime.now()
        # datetime object containing current date and time

        # dd_mm_YY__H_M_S
        dt_string = now.strftime("%d_%m_%Y__%H_%M_%S")
        FontSize = int(input("Enter Font size: "))
        WPM = int(input("Enter Words per Minute: "))
        usrCFGfile = str("config_" + dt_string + ".cfg")
        userconfig = open(usrCFGfile, "w")
        userconfig.writelines("FontSize=" + str(FontSize))
        userconfig.writelines("WordsPerMinute=" + str(WPM))
        print("User config saved in " + usrCFGfile)
        userconfig.close()
        return (FontSize, WPM)

    def GetFontSize(self):
        return self.FontSize

    def getWPM(self):
        return self.WPM


# This code snippet now flashes the words per minute.

cofg = configuration()
para = open("para.txt", "r")
words = [str(x) for x in para.read()]

'''
def nextword():
    for word in words:
        yield word
'''


def WordPerSecond():
    return cofg.getWPM() / 60


WPS = WordPerSecond()

root = tk.Tk()
root.attributes("-fullscreen", True)
root.bind("<F11>", lambda event: root.attributes("-fullscreen", not root.attributes("-fullscreen")))
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))
root.bind("<F1>", lambda event: exit(0))

w = tk.StringVar()

labelFlash = tk.Label(root, bg='Black', width=root.winfo_screenwidth(), height=root.winfo_screenheight(),
                      anchor="center", text="Sample", fg="White", font="Times " + str(cofg.GetFontSize()), textvariable=w)
labelFlash.pack()
for word in words:
    w.set(word)
"""
    labelFlash["text"] = word
    labelFlash.after(int(WPS))  # labelFlash.update_idletasks())
"""

'''
canvasFlash = tk.Canvas(root, bg='Black', width=root.winfo_screenwidth(), height=root.winfo_screenheight())
canvasFlash.pack()

for w in words:
    word = tk.StringVar(canvasFlash, value=str(w))
    wordID = canvasFlash.create_text(root.winfo_screenwidth() / 2, root.winfo_screenheight() / 2,
                                     anchor="center", fill="white", font="Times " + str(cofg.GetFontSize()), text=word)
    canvasFlash.after(int(WPS), canvasFlash.update_idletasks())
    # canvasFlash.destroy()
    # canvasFlash.update_idletasks()
    # canvasFlash.config(text=str(word))
'''
'''
# , text="Starting in 5 sec!"
# sleep(5) commented for faster testing.
# for word in words:
canvasFlash.itemconfigure(wordID, text=nextword())
# canvasFlash.insert(wordID, cofg.GetFontSize(), word)
canvasFlash.after(WPS, nextword())
# sleep(WPS)
'''
root.mainloop()
