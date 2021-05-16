
import random
import gamevalue

def rolldice():
    return random.randint(1, 6)

def makeMove(tokenobj, boardobj):
    oldpos = tokenobj.getPosition()
    val = rolldice()
    tokenobj.incrPosition(val)
    pos = tokenobj.getPosition()
    cityname = boardobj.getCellName(pos)
    city = boardobj.fetchCity(cityname)
    if pos - oldpos <= 0:
        # credit salary
        tokenobj.credit(int( boardobj.fetchCity("Start")["rent"] ) )
        print('points credited')
        tokenobj.printInfo()
    # print status update
    print(f'dice roll: {val} |', end=' ')
    print(f'{tokenobj.getName()} reaches {cityname:x>10} belongs to {city["owner"]:x>6} with rent {city["rent"]}')
    return city

def play(tokenobj, boardobj):
    pname = tokenobj.getName()
    city = makeMove(tokenobj, boardobj)
    price = int(city["price"])
    if city["type"] in gamevalue.buyable and city["owner"] == "Banker":
        # ask to buy
        tokenobj.printInfo()
        choice = input(f'do you wish to buy {city["name"]:x>10} for {price} <y/n>:')
        if choice not in ('y', 'Y'): return
        if tokenobj.checkBalance(price):
            tokenobj.debit(price)
            tokenobj.addWealth(price)
            boardobj.setOwner(city["name"], pname)
        tokenobj.printInfo()
    elif city["type"] == "Tax":
        # calculate tax
        pass
    elif city["owner"] == pname:
        print(f'its my city')
    else:
        # pay rent to city owner
        pass
    boardobj.printAllCities()
    