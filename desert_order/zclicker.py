
import pyautogui as m
import desert_utilities as u
import argparse

from pynput import mouse 
from time import sleep
from datetime import datetime


def mouseListener():
    listener = mouse.Listener(on_click=u.on_click)
    listener.start()
    listener.join()
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--delay", 
        type=int, 
        help="delay to be added to 'timer'")
    parser.add_argument("-i", "--increment",
        type=int,
        help="increase time by mentioned amount after every rounds.")

    args = parser.parse_args()
    buf_timer = args.delay if args.delay else 2
    incrementer = args.increment if args.increment else 0

    x = y = 0
    while True:
        print("[=] Right-Click to accept, else left-click again.")
        mouseListener()
        if u.SD.is_success:
            x, y = u.SD.point.x, u.SD.point.y 
            break
    
    print(f"x:{x}, y:{y}")
    t1 = datetime.now()
    
    timer = int(input("[=] wait timer    : ")) + buf_timer
    qty = int(input("[=] enter quantity: "))
    
    td = datetime.now() - t1
    
    flag = True
    to_wait = timer

    for count in range(1, qty):
        msg = "completed qty will: {}".format(count)

        m.move(-2, 0)
        if not flag:
            to_wait = timer
            timer += incrementer
        else:
            flag = False
            to_wait = max(timer - td.seconds, buf_timer)
            # if count % 2 == 0:
            # buf_timer += incrementer

        u.countdown(to_wait, msg)
        m.click(x, y)

    print("\n[=] exiting...")