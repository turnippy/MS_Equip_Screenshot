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

from pynput import mouse
from time import sleep


def get_coords():
    return


def main(out_dir=None):
    if not out_dir:
        print("invalid output directory")
        return
    out_path = os.path.join(os.getcwd(), out_dir)
    try:
        os.mkdir(out_path)
    except FileExistsError:
        pass
    print("Saving output to", out_path)
    get_coords()

    input("Press any key to exit...")
    return


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("invalid number of command line args")
        print("usage: python main.py \"destination folder name\"")
        input("Press any key to exit...")
        exit()
    main(sys.argv[1])
