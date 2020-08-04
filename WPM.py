from datetime import datetime
from time import sleep


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
            file.writelines(["FontSize=50\n", "WordsPerMinute=30"])
        finally:
            print("Words Per Minute!\n")
            print("1. Use Default Config?")

    def UserConfiguration():

        now = datetime.now()
        # datetime object containing current date and time

        # dd_mm_YY__H_M_S
        dt_string = "config" + now.strftime("%d_%m_%Y__%H_%M_%S")
        FontSize = int(input("Enter Font size: "))
        WPM = int(input("Enter Words per Minute: "))
        usrCFGfile = str("config" + dt_string + ".cfg")
        userconfig = open(usrCFGfile, "w")
        userconfig.writeline("FontSize=" + str(FontSize))
        userconfig.writeline("WordsPerMinute=" + str(WPM))
        print("User config saved in " + usrCFGfile)
