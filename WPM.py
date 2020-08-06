import os
import tkinter as tk


class configuration():
    def __init__(self):
        self.FontSize = 0
        self.WPS = 0
        print("Words Per Minute!\n")
        print("\nUse <Escape> or <F11> to manipulate the window's fullscreen properties!\n\n")
        self.FontSize, self.WPS = self.UserConfiguration()
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

    def UserConfiguration(self):
        self.FontSize = int(input("Enter Font size (100 recommended): "))
        self.WPS = int(input("Enter Words per Second (Higher the number, faster the words display): "))
        return (self.FontSize, self.WPS)

    def GetFontSize(self):
        return int(self.FontSize)

    def getWPS(self):
        return int(self.WPS)


# This code snippet now flashes the words per minute.
cofg = configuration()
para = open("para.txt", "r")
words = [str(x) for x in para.read().split()]


def Miliseconds_per_word():
    return 1000 / cofg.getWPS()


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
