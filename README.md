Valentine Project
This program is designed to display a beautiful animation of flowers on the screen, intended for special occasions like Valentine's Day. It checks whether a specified program (e.g., Outlook or Telegram) is running, and if it's the right day (such as March 8th), it triggers a fun flower animation. Additionally, the program includes features for autostart and the option to close the specified program automatically at a scheduled time.

Features
Flower Animation: Displays multiple colorful flowers on the screen.
Auto Start: Adds the program to the Windows autostart for convenience.
Program Monitoring: Checks whether a selected program (e.g., Outlook or Telegram) is running and closes it at a scheduled time.
Date-based Trigger: Launches the animation on a specific date (e.g., March 8th).
Customizable: Allows changing the color, size, and number of flowers. The program also checks whether specific programs are open and can close them if needed.
Requirements
Python 3.x: Make sure Python is installed.
Required Libraries:
tkinter: for GUI and flower animation.
pygetwindow: for working with windows and closing programs.
screeninfo: to get screen dimensions.
winreg: to interact with Windows registry for autostart.
pygetwindow: for window management (closing specified programs).
time, locale, random, os, sys: various utility libraries.
Install dependencies:
bash
Копировать код
pip install pygetwindow screeninfo
Usage
Autostart: The program will automatically check if it's set to start on system boot. If not, it will add itself to the autostart list.

Flower Animation: On the specified day (e.g., March 8th), the program will trigger an animation of flowers on the screen. The flowers' colors, size, and number are customizable.

Closing Programs: The program checks if the selected program (e.g., Outlook) is running. It will close the program at a set time (e.g., 11:00 PM).

Exit: To close the program, press the keys 'q' or 'й'.

Configuration
You can change the following settings:

launch_date: Set the specific day for triggering the flower animation (default is March 8th).
close_time: Set the time when the program should attempt to close the selected program (default is 11:00 PM).
FLOWER_NUMBER: Set how many flowers should appear at once.
MAX_FLOWER_SIZE: Set the maximum size of the flowers.
EXIT_BUTTON: Change the key(s) that exit the program.
How It Works
Autostart: The program checks the Windows registry to see if it has been added to the autostart list. If not, it adds itself to ensure it runs on startup.

Flower Animation: When the specified date arrives, the program generates a random number of flowers on the screen. The flowers vary in color, size, and position. The animation runs in a loop until you press 'q' or 'й' to exit.

Program Monitoring and Closing: The program monitors the selected program and checks if it's running. If the program is running on the specified date and time, the program closes it.

Exit: Press 'q' or 'й' to exit the program at any time.

License
This project is licensed under the MIT License - see the LICENSE file for details.
