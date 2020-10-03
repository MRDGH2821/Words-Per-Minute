from cx_Freeze import Executable, setup

setup(name="Words Per Minute!",
      version="1.0.1",
      description="This program lets you display a paragraph, word by word; in full screen!",
      executables=[Executable("WPM.py")])
