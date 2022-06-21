# -*- coding: utf-8 -*- 

import desert_code as d
import desert_utilities as u


def options(action_list):    
    print(
        " \t 0. Exit \n" 
        " \t 1. New Clicker \n"
        " \t 2. Track mouse position \n", end='')
    for index, obj in enumerate(action_list, start=3):
        print(f" \t {index}. {obj.name}")
    
    return int(input("\n[=] choice: "))


if __name__ == "__main__":
    action_list = []
    # action_list =[
    #     DesertActionData("North Ammo", DesertPoint(1722, 131), DesertPoint(1103,778), 20 ),
    #     DesertActionData("NorthEast Breda", DesertPoint(1747, 160), DesertPoint(1339, 622), 35 ),
    # ]
    u.getDataFiles()
    print(f"[=] attempt to read {u.SD.datafile}")
    action_list = u.parseDataFile()

    try:
        desert = d.DesertMain()
        while True:
            choice = options(action_list)

            if choice == 0:
                print("[=] exiting...")
                break
            if choice == 1:
                desert.newClicker(action_list)
            elif choice == 2:
                desert.trackPosition()
            elif choice >= 3 and choice <= len(action_list)+3:
                qty = int(input("[=] enter quantity: "))
                u.countdown(5, "starting in")
                desert.production(action_list[choice - 3], qty)
            else:
                foobar = None
            
    except KeyboardInterrupt as e:
        print("[x] Exception caught: {}".format(e))
        print("[x] exiting...")
    
    finally:
        u.saveDataFile(action_list)
        print("[=] program terminate \n")
