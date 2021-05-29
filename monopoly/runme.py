
import player
# import card
import board
# import gamevalue
import processturn
from utils import highlighter


if __name__ == "__main__":
    myboard = board.Board('config.xml')
    banker = player.Player("Banker")    # required to collect Tax and Fees
    myboard.parseConfig(banker)
    myboard.printAllCities()

    red = player.Player("Red")
    blue = player.Player("Blue")
    green = player.Player("Green")
    yellow = player.Player("Yellow")
    participants = (red, green, blue)
    turn=0
    try:
        while True:
            # var = input(f"{turn} enter to continue: ")
            turn += 1
            gameover = 0
            for token in participants:
                if not token.isActive(): continue
                gameover += 1
                vartext = f"[{token.getName():6}] {token.getPosition():02} | " + \
                    f"trip {token.getTrip()} round {turn}  " + \
                    f"press enter: "
                # print(f">{vartext}<")
                vartext = highlighter(vartext)
                vartext = input(f"{vartext}")
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

# -- END --