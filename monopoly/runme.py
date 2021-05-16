
import player
import card
import board
import gamevalue
import utils


if __name__ == "__main__":
    myboard = board.Board('config.xml')
    myboard.parseConfig()
    for c in gamevalue.cardcolor:
        myboard.printCity(c)

    red = player.Player("Red")
    blue = player.Player("Blue")
    green = player.Player("Green")
    yellow = player.Player("Yellow")

    turn=0
    while turn < 10:
        var = input(f"{turn} enter to continue: ")
        turn += 1
        city = utils.play(red, myboard)