
import player
import card
import board
import gamevalue
import utils


if __name__ == "__main__":
    myboard = board.Board('config.xml')
    myboard.parseConfig()
    myboard.printAllCities()

    myboard.printCity("Red")

    red = player.Player("Red")
    blue = player.Player("Blue")
    green = player.Player("Green")
    yellow = player.Player("Yellow")

    turn=0
    try:
        while turn < 12:
            # var = input(f"{turn} enter to continue: ")
            turn += 1
            utils.play(red, myboard)
            utils.play(green, myboard)
    except KeyboardInterrupt as e:
        print('\ncaught user interrupt Ctrl+C, exiting...')

# -- END --