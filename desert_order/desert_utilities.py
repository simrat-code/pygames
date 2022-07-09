# -*- coding: utf-8 -*-

import json
import os
import glob
import desert_code as d
import desert_point as dp
from time import sleep
from pynput import mouse


class SD:
    #
    # shared-data
    #
    is_data_change = False
    is_success = False              # for misc use, as a flag
    datapath = "data"
    datafile = "data/base_info.txt"
    point = dp.DesertPoint(0, 0)   # use to save the 'clicking  location'


def on_click(x, y, button, pressed):
    SD.is_success = False
    if button == mouse.Button.left:
        print(f"[=] left click at {x} {y}")
        SD.point.x = x 
        SD.point.y = y 
    elif button == mouse.Button.right:
        SD.is_success = True
    return False


def getDataFiles():
    data = {0: "new file"}
    for index, f in enumerate(sorted(glob.glob(os.path.join(SD.datapath, "*.txt"))), start=1):
        data[index] = f

    while True:
        for k, v in data.items():
            print(f"\t {k}. {v}")
        choice = int(input("\n[=] enter choice: "))
        try:
            data[choice]
        except KeyError: continue
        else: break
    if choice == 0:
        fname = input("enter new data-file name: ").lower()
        if not fname.endswith(".txt"): fname = fname + ".txt"
        SD.datafile = os.path.join(SD.datapath, fname)
        with open(SD.datafile, "w") as fp: pass 
    else:
        SD.datafile = data[choice]


def parseDataFile():
    if os.stat(SD.datafile).st_size == 0: return []
    action_list = []
    with open(SD.datafile) as jsonfile:
        jobj = json.load(jsonfile)
        for key in jobj:
            tmp_obj = d.DesertActionData(**key)
            action_list.append(tmp_obj)
    return action_list


def saveDataFile(action_list):
    if len(action_list) == 0:
        print(f"[=] action list is empty, not saving... ")
        return

    if not SD.is_data_change:
        return

    print(f"\n\n[=] Save Sequence, displaying list of click-actions")
    for obj in action_list:
        print(f"\t {obj.name}")
    choice = input("[=] do you want to save the list, <y/n>: ")
    if choice not in ['y', 'Y']: return

    print("saving data ...")
    with open(SD.datafile, "w") as outfp:
        json.dump(
            [obj for obj in action_list], 
            outfp, 
            indent=4, 
            cls=d.DesertMainEncoder)
    SD.is_data_change = False



def countdown(val, msg="waiting"):
    while val >= 0:
        print(f"\r{msg}: {val}    ", end='')
        sleep(1)
        val -= 1
    print("\r", " "*40, end='')


# -- END --