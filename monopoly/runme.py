
import player
import card
import board
import gamevalue

if __name__ == "__main__":
    myboard = board.Board('config.xml')
    myboard.parseConfig()
    for c in gamevalue.cardcolor:
        myboard.printCity(c)