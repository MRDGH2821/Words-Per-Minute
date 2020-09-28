import tkinter as tk
from sys import exit


class configuration():
    def __init__(self):
        self.FontSize = 0
        self.WPS = 0
        print("Words Per Minute!\n")
        print("\nUse <Escape>, <F11> or <F1> to manipulate the window's fullscreen properties!\n\n")
        self.FontSize, self.WPS = self.UserConfiguration()
        try:
            para = open("para.txt", "r")
            if not para:
                para.close()
                raise FileNotFoundError
            else:
                choice = 0
                choice = int(
                    input("\n0. Use existing para?\n1. Make new para? \nEnter choice (0 Default): "))
                if choice:
                    raise FileNotFoundError
                else:
                    para.close()
        except FileNotFoundError:
            para = open("para.txt", "w")
            print("Enter/Paste your content. To save it - <Ctrl + D + Enter> or <Ctrl + Z + Enter> ( Windows ).")
            while True:
                try:
                    line = input()
                except EOFError:
                    break
                para.write(line)
            para.close()

        except ValueError:
            para.close()

    def UserConfiguration(self):
        print("Configuration Menu:\n\n")
        try:
            self.FontSize = int(input("Enter Font size (100 default): "))
        except ValueError:
            self.FontSize = 100
        try:
            print("\nYou might be Familier with Words per minute.\nThis program internally uses Words per Second convention.\nPlease Divide WPM by 60 and enter the value here.\nDefault Value is 2 WPS, i.e. 120 WPM.\n")
            self.WPS = float(input("Enter Words per Second (Higher the number, faster the words display): "))
        except ValueError:
            self.WPS = 2

        return (self.FontSize, self.WPS)

    def GetFontSize(self):
        return int(self.FontSize)

    def getWPS(self):
        return float(self.WPS)


# This code snippet now flashes the words per minute.
cofg = configuration()
input("Before proceeding, remember:\n - <Escape> will close the program\n - <F1> will force fully exit fullscreen\n - <F11> will toggle between fullscreen & windowed mode.\n\n**Keys will work after mouse click**\n\n\nPress enter to continue!")
para = open("para.txt", "r")
words = [str(x) for x in para.read().split()]


def Miliseconds_per_word():
    return 1000 / cofg.getWPS()


MPW = Miliseconds_per_word()
root = tk.Tk()
root.attributes("-fullscreen", True)
root.bind("<F11>", lambda event: root.attributes("-fullscreen", not root.attributes("-fullscreen")))
root.bind("<F1>", lambda event: root.attributes("-fullscreen", False))
root.bind("<Escape>", lambda event: exit())
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
