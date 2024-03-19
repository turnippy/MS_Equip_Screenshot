"""
Usage:
    python main.py "destination folder name"

This script does:
    1. Find coord on screen of Maplestory.exe.
    2. Find coord of anchor (equip inventory).
    3. Using hard-coded relative position to anchor, mouse over and print screen.
    4.
"""
import copy
import sys
import os
import mss
import cv2
import numpy as np

from win32gui import FindWindow, GetWindowRect
from pynput.mouse import Controller
from time import sleep

ANCHOR_TOTEM_OFFSET = [-45, 15]
ANCHOR_ITEM_OFFSET = [20, 45]
ITEM_SLOT_OFFSET = 42
ITEM_COLS = [
    ["ring1", "ring2", "ring3", "ring4", "pocket"],
    [None, "pendant1", "pendant2", "weapon", "belt"],
    ["hat", "face", "eye", "top", "bottom", "shoe"],
    [None, None, "ear", "shoulder", "gloves"],
    ["emblem", "badge", None, "secondary", "cape", "heart"]
]


def get_rect():
    """
    :return: coordinates of "MapleStory" window in a dict with keys "left", "top", width", height"
    """
    window_handle = FindWindow(None, "MapleStory")
    try:
        window_rect = GetWindowRect(window_handle)
    except BaseException:
        input("Window not found.\nPress any key to exit...")
        exit()
    rect = {"left": window_rect[0], "top": window_rect[1],
            "width": window_rect[2] - window_rect[0], "height": window_rect[3] - window_rect[1]}
    return rect


def get_anchor(img_in):
    """
    :param img_in: numpy array representing 3 channels for image
    :return: left,top representing coordinates of anchor relative to img_in
    template matching is done with cv2.matchTemplate()
    correlation is calculated using CCOEFF_NORMED
    """
    img_gray = cv2.cvtColor(img_in, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(os.path.join(os.getcwd(), 'resources/equip_window_anchor.png'), cv2.IMREAD_GRAYSCALE)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    # look for local max (threshold > 0.75) when using CCOEFF_NORMED

    return np.where(res >= 0.75)[1], np.where(res >= 0.75)[0]


def screenshot(rect=None, fn=None):
    """
    :param rect: takes a dict with keys "left", "top", width", height"
    :param fn: abs path to image file location
    :return: np array with 3 channels representing screenshot of the area enclosed by "rect"
    saves as filename = fn if one is provided
    """
    if not rect:
        raise ValueError("Invalid coordinates passed to screenshot.")
    with mss.mss() as sct:
        img = np.array(sct.grab(rect))
        if fn:
            cv2.imwrite(fn, img)

    return img


def take_screenshots(outpath, ms_coords, anchor_loc):
    """
    :param outpath: abs path output image folder
    :param ms_coords: dict with keys left, top, width, height corresponding to absolute coordinates of MS on screen
    :param anchor_loc: list with [left, top] corresponding to absolute coordinate of anchor on screen
    :return: none
    iterates through each item slot position and totem position, takes a screenshot, and saves to out_dir
    """
    m = Controller()

    # totem slots

    curr = copy.deepcopy(anchor_loc)
    curr[0] += ANCHOR_TOTEM_OFFSET[0]
    curr[1] += ANCHOR_TOTEM_OFFSET[1]

    for i in [1, 2, 3]:
        m.position = curr
        sleep(0.25)
        img = screenshot(rect=ms_coords, fn=os.path.join(outpath, f'totem{i}.png'))
        curr[1] += ITEM_SLOT_OFFSET
        print(f"\tTotem {i} done")

    curr = copy.deepcopy(anchor_loc)
    curr[0] += ANCHOR_ITEM_OFFSET[0]
    curr[1] += ANCHOR_ITEM_OFFSET[1]

    # item slots
    for col in ITEM_COLS:
        for item in col:
            if item:
                m.position = curr
                sleep(0.25)
                img = screenshot(rect=ms_coords, fn=os.path.join(outpath, f'{item}.png'))
            curr[1] += ITEM_SLOT_OFFSET  # Move down column
        curr[0] += ITEM_SLOT_OFFSET  # Move to next column


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

    ms_coords = get_rect()
    ms_img = screenshot(rect=ms_coords)

    anchor_left, anchor_top = get_anchor(ms_img)
    anchor_coords_abs = [(anchor_left + ms_coords['left']), (anchor_top + ms_coords['top'])]

    take_screenshots(out_path, ms_coords, anchor_coords_abs)

    input("Completed! Press any key to exit...")
    return


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("invalid number of command line args")
        print("usage: python main.py \"destination folder name\"")
        input("Press any key to exit...")
        exit()
    main(sys.argv[1])
