
import json 
import pyautogui as m
from time import sleep
from json import JSONEncoder
from pynput import mouse


is_data_change = False

class DesertPoint:
    def __init__(self, x, y):
        self.x = x 
        self.y = y 

    def __str__(self):
        return "{} {}".format(self.x, self.y)

    def __getitem__(self, key):
        if key == 'x': return self.x 
        elif key == 'y': return self.y 
        else: KeyError("Execption: passed key does not exist in DesertPoint object")




point = DesertPoint(0, 0)
datafile = "base_info.txt"


def on_click(x, y, button, pressed):
    if button == mouse.Button.left:
        print(f"[=] left click at {x} {y}")
        point.x = x 
        point.y = y 
    return False


def countdown(val, msg="waiting"):
    while val >= 0:
        print(f"\r{msg}: {val}    ", end='')
        sleep(1)
        val -= 1
    print("\r", " "*40)


class DesertActionData:
    def __init__(self,  name="action_name",
                        mini_map_xy=DesertPoint(0,0),
                        action_xy=DesertPoint(0,0),
                        action_timer=10 ) -> None:

        self.name = name
        self.mini_map_xy = mini_map_xy  # dict{'x': 0, 'y': 0}
        self.action_xy = action_xy      # dict{'x': 0, 'y': 0}
        self.action_timer = action_timer

    def getName(self): return self.name
    def getMiniMapXY(self): return self.mini_map_xy['x'], self.mini_map_xy['y'] 
    def getActionXY(self): return self.action_xy['x'], self.action_xy['y']    
    def getActionTimer(self): return self.action_timer



class DesertMain:
    def __init__(self):
        self.verify_timer = 5

    def trackPosition(self):
        while True:
            print("\rposition {}    ".format(m.position()), end='')
            sleep(0.5)


    def production(self, act_obj, qty=1):
        if not isinstance(act_obj, DesertActionData):
            raise ValueError("act_obj must be of ActionDesertData")
        
        for c in range(1, qty+1):
            x, y = act_obj.getMiniMapXY()
            # print(f"\n\n {act_obj.getMiniMapXY()} \n\n")
            # break
            #
            m.click(x, y)
            sleep(1)
            x, y = act_obj.getActionXY()
            m.moveTo(x, y)

            self._click2cook()
            if x > 500: self._screenMove(400, 0)
            else: self._screenMove(0, 400)

            if c == qty: break          # no need to wait, production already started.
            countdown(act_obj.getActionTimer() - self.verify_timer, "{}: {}/{}, waiting".format(act_obj.name, c, qty))
        print(f"\r[=] production of {act_obj.name}, qty: {qty}, has been completed")


    def _click2cook(self):
        #
        # wait for buffer time
        # it should give enough time to correct the position, in case:
        #   1) in case of miss/wrong selection (left/right)
        #   2) in case of captcha
        #
        countdown(8, "about to CLICK in")
        m.click()
        countdown(self.verify_timer, "verify production")


    def _screenMove(self, x, y):
        m.mouseDown(button="right")
        m.move(x, y)
        m.mouseUp(button="right")


    def newClicker(self, obj_list):
        name = input("action name: ")
        map_xy = DesertPoint(0,0)
        res_xy = DesertPoint(0,0)

        while True:
            print("[=] click on mini-map to see BASE on screen")
            listener = mouse.Listener(on_click=on_click)
            listener.start()
            listener.join()
            choice = input(f"if above location is correct <y/n>: ")
            if choice in ['y', 'Y', 'yes', 'Yes']: 
                map_xy.x, map_xy.y = point.x, point.y 
                break

        while True:
            print("[=] hover and click, on resource to produce")
            listener = mouse.Listener(on_click=on_click)
            listener.start()
            listener.join()
            choice = input(f"if above location is correct <y/n>: ")
            if choice in ['y', 'Y', 'yes', 'Yes']: 
                res_xy.x, res_xy.y = point.x, point.y 
                break

        duration = int(input("[=] enter production time: "))

        obj = DesertActionData(name, map_xy, res_xy, duration)
        choice = input("[=] add to list, <y/n>: ")
        if choice in ['y', 'Y']: 
            obj_list.append(obj)
            is_data_change = True
        qty = int(input("[=] enter quantity: "))
        countdown(duration, "as res already building")
        self.production(obj, qty)


class DesertMainEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def options(action_list):    
    print(
        " \t 0. Exit \n" 
        " \t 1. New Clicker \n"
        " \t 2. Track mouse position \n", end='')
    for index, obj in enumerate(action_list, start=3):
        print(f" \t {index}. {obj.name}")
    
    return int(input("\n[=] choice: "))


def parseDataFile():
    action_list = []
    with open(datafile) as jsonfile:
        jobj = json.load(jsonfile)
        for key in jobj:
            tmp_obj = DesertActionData(**key)
            action_list.append(tmp_obj)
    return action_list


def saveDataFile(action_list):
    if len(action_list) == 0:
        print(f"[=] action list is empty, not saving... ")
        return

    if not is_data_change:
        return

    print(f"\n\n[=] Save Sequence, displaying list of click-actions")
    for obj in action_list:
        print(f"\t {obj.name}")
    choice = input("[=] do you want to save the list, <y/n>: ")
    if choice not in ['y', 'Y']: return

    print("saving data ...")
    with open(datafile, "w") as outfp:
        json.dump(
            [obj for obj in action_list], 
            outfp, 
            indent=4, 
            cls=DesertMainEncoder)


 

if __name__ == "__main__":
    action_list = []
    # action_list =[
    #     DesertActionData("North Ammo", DesertPoint(1722, 131), DesertPoint(1103,778), 20 ),
    #     DesertActionData("NorthEast Breda", DesertPoint(1747, 160), DesertPoint(1339, 622), 35 ),
    # ]
    print(f"[=] attempt to read {datafile}")
    action_list = parseDataFile()

    try:
        desert = DesertMain()
        choice = options(action_list)

        if choice == 1:
            countdown(3, "starting in")
            desert.newClicker(action_list)
        elif choice == 2:
            desert.trackPosition()
        elif choice >= 3 and choice <= len(action_list)+3:
            qty = int(input("[=] enter quantity: "))
            countdown(5, "starting in")
            desert.production(action_list[choice - 3], qty)
        else:
            foobar = None
        
    except KeyboardInterrupt as e:
        print("[x] Exception caught: {}".format(e))
        print("[x] exiting...")
    
    finally:
        saveDataFile(action_list)
        print("[=] program terminate \n")
