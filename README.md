# Valentine Project

This program is designed to display a beautiful animation of flowers on the screen, intended for special occasions like Valentine's Day. It checks whether a specified program (e.g., Outlook or Telegram) is running, and if it's the right day (such as March 8th), it triggers a fun flower animation. Additionally, the program includes features for autostart and the option to close the specified program automatically at a scheduled time.

## Features

- **Flower Animation**: Displays multiple colorful flowers on the screen.
- **Auto Start**: Adds the program to the Windows autostart for convenience.
- **Program Monitoring**: Checks whether a selected program (e.g., Outlook or Telegram) is running and closes it at a scheduled time.
- **Date-based Trigger**: Launches the animation on a specific date (e.g., March 8th).
- **Customizable**: Allows changing the color, size, and number of flowers. The program also checks whether specific programs are open and can close them if needed.

## Requirements

- **Python 3.x**: Make sure Python is installed.
- **Required Libraries**:
  - `tkinter`: for GUI and flower animation.
  - `pygetwindow`: for working with windows and closing programs.
  - `screeninfo`: to get screen dimensions.
  - `winreg`: to interact with Windows registry for autostart.
  - `pygetwindow`: for window management (closing specified programs).
  - `time`, `locale`, `random`, `os`, `sys`: various utility libraries.
  
  **Install dependencies**:  
  ```bash
  pip install pygetwindow screeninfo
