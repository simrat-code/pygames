# -*- coding: utf-8 -*-


import json 
import pyautogui as m
import desert_utilities as u
import desert_point as dp
from time import sleep
from json import JSONEncoder
from pynput import mouse


class DesertActionData:
    def __init__(self,  name="action_name",
                        mini_map_xy=dp.DesertPoint(0,0),
                        action_xy=dp.DesertPoint(0,0),
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
            u.countdown(act_obj.getActionTimer() - self.verify_timer, "{}: {}/{}, waiting".format(act_obj.name, c, qty))
        print(f"\r[=] production of {act_obj.name}, qty: {qty}, has been completed")


    def _click2cook(self):
        #
        # wait for buffer time
        # it should give enough time to correct the position, in case:
        #   1) in case of miss/wrong selection (left/right)
        #   2) in case of captcha
        #
        u.countdown(8, "about to CLICK in")
        m.click()
        u.countdown(self.verify_timer, "verify production")


    def _screenMove(self, x, y):
        m.mouseDown(button="right")
        m.move(x, y)
        m.mouseUp(button="right")


    def _mouseListener(self):
        listener = mouse.Listener(on_click=u.on_click)
        listener.start()
        listener.join()


    def newClicker(self, obj_list):
        name = input("action name: ")
        map_xy = dp.DesertPoint(0,0)
        res_xy = dp.DesertPoint(0,0)

        print("[=] click on mini-map to see BASE on screen")
        self._mouseListener()
        while True:
            print("[=] Right-Click to accept, else left-click again.")
            self._mouseListener()
            # choice = input(f"if above location is correct <y/n>: ")
            # if choice in ['y', 'Y', 'yes', 'Yes']: 
            if u.SD.is_success:
                map_xy.x, map_xy.y = u.SD.point.x, u.SD.point.y 
                break

        print("[=] hover and click, on resource to produce")
        self._mouseListener()
        while True:
            print("[=] Right-Click to accept, else left-click again.")
            self._mouseListener()
            # choice = input(f"if above location is correct <y/n>: ")
            # if choice in ['y', 'Y', 'yes', 'Yes']: 
            if u.SD.is_success:
                res_xy.x, res_xy.y = u.SD.point.x, u.SD.point.y 
                break

        duration = int(input("[=] enter production time: "))

        obj = DesertActionData(name, map_xy, res_xy, duration)
        choice = input("[=] add to list, <y/n>: ")
        if choice in ['y', 'Y']: 
            obj_list.append(obj)
            u.SD.is_data_change = True
        qty = int(input("[=] enter quantity: "))
        u.countdown(duration, "as res already building")
        self.production(obj, qty)


class DesertMainEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

# -- END --
