
import player
# import card
import board
# import gamevalue
import processturn


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
                var = input(f"\n[{token.getNameC():6}] trip {token.getTrip()} round {turn}  press enter: ")
                processturn.play(token, myboard)
            # IF only one player is left, declare it winner
            if gameover <= 1: break

        for x in participants:
            if x.isActive: 
                x.printInfo()
                print(f'Winner is {x.getNameC()} !!!')
                break
    except KeyboardInterrupt as e:
        print('\ncaught user interrupt Ctrl+C, exiting...')

# -- END --