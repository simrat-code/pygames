
import player
import board
import processturn
from utils import highlighter
from utils import colorText

def printPosition(participants):
    if not isinstance(participants, tuple): raise TypeError("must pass tuple")
    # print(" "*8, end="")
    for obj in participants:
        if not isinstance(obj, player.Player): continue
        print(
            colorText(
                f"{obj.getPosition():02} {obj.getIncome():>5}", obj.name
            )
            , end="  "
        )
    # print("")

def main():
    myboard = board.Board('config.xml')
    banker = player.Player("Banker")    # required to collect Tax and Fees
    myboard.parseConfig(banker)
    myboard.printAllCities()

    red = player.Player("Red")
    blue = player.Player("Blue")
    green = player.Player("Green")
    yellow = player.Player("Yellow")
    participants = (red, green, blue, yellow)
    turn=0
    try:
        while True:
            turn += 1
            gameover = 0
            for token in participants:
                if not token.isActive(): continue
                gameover += 1
                print(
                    highlighter(
                        f"[{token.getName():6}] "
                    )
                    , end=""
                )
                printPosition(participants)
                vartext = input("press enter: ")
                processturn.play(token, myboard)
            # IF only one player is left, declare it winner
            if gameover <= 1: break

        for x in participants:
            if x.isActive: 
                x.printInfo()
                print(
                    highlighter(
                        f'Winner is {x.getName()} !!!'
                    )
                )
                break
    except KeyboardInterrupt as e:
        print('\ncaught user interrupt Ctrl+C, exiting...')
    finally:
        print(f"total turns: {turn}\n")

