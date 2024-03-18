'''
Usage:
    python main.py "destination folder name"

This script does:
    1. Find coord on screen of Maplestory.exe.
    2. Find coord of anchor (equip inventory).
    3. Using hard-coded relative position to anchor, mouse over and print screen.
    4.
'''

import sys
import os
import mss
import cv2
import numpy

from win32gui import FindWindow, GetWindowRect
from pynput import mouse
from time import sleep


def get_MS_xy():
    coords = []
    return coords


def screenshot(xy=None):
    if not xy:
        raise ValueError("Invalid coordinates passed to screenshot.")
    with mss.mss() as sct:
        pass



def main(out_dir=None):

    if not out_dir:
        input("Invalid output directory.\nPress any key to exit...")
        return
    out_path = os.path.join(os.getcwd(), out_dir)
    try:
        os.mkdir(out_path)
    except FileExistsError:
        pass
    print("Saving output to", out_path)

    ms_coords = get_MS_xy()
    if not ms_coords:
        input("MS Window not found.\nPress any key to exit...")
        return

    input("Press any key to exit...")
    return


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("invalid number of command line args")
        print("usage: python main.py \"destination folder name\"")
        input("Press any key to exit...")
        exit()
    main(sys.argv[1])
