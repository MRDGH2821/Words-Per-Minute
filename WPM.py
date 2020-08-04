from datetime import datetime
from time import sleep
import tkinter as tk
import os


class configuration():

    def __init__(self):
        FontSize = 0
        WPM = 0
        try:
            config = open("default.cfg", "r")
            FontSize = config.readline()[-2:]
            WPM = config.readline()[-2:]
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
        para = open("para.txt", "w")
        os.startfile("para.txt")
        print("Write your words in para.txt\n\n")
        para.close()
        print("Use <F11> to enter into Fullscreen, <Esc> to exit fullscreen\n ")

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
"""
class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master = master
        pad = 3
        self._geom = '200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth() - pad, master.winfo_screenheight() - pad))
        master.bind('<Escape>', self.toggle_geom)

    def toggle_geom(self, event):
        geom = self.master.winfo_geometry()
        print(geom, self._geom)
        self.master.geometry(self._geom)
        self._geom = geom
"""

cofg = configuration()
para = open("para.txt", "r")
words = para.read()
root = tk.Tk()
root.attributes("-fullscreen", True)
root.bind("<F11>", lambda event: root.attributes("-fullscreen",
                                                 not root.attributes("-fullscreen")))
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))
"""
top.geometry()
top.attributes("-fullscreen", True)
top.bind('<Escape>', top.attributes("-fullscreen", False))
"""
# WPMFlash = FullScreenApp(top)
WPMFlash = tk.Frame(root)
WPMFlash.pack()

root.mainloop()
