
import random
import gamevalue

def rolldice():
    return random.randint(1, 6)

def makeMove(tokenobj, boardobj):
    """ Returns cityobj """
    oldpos = tokenobj.getPosition()
    pos = tokenobj.incrPosition(rolldice())
    cityobj = boardobj.getCellObject(pos)
    # cityname = cityobj.getName()
    # city = boardobj.fetchCity(cityname)
    if pos - oldpos <= 0:
        # credit salary
        tokenobj.credit( boardobj.getCellObject(0).getRent() )
        print(f'[{tokenobj.getName():6}]', 'points credited')
        tokenobj.printInfo()
    print(f'[{tokenobj.getName():6}]', f'dice roll: {tokenobj.getDice()} | reaches', cityobj.getBelong() )
    return cityobj

def play(tokenobj, boardobj):
    pname = tokenobj.getName()
    cityobj = makeMove(tokenobj, boardobj)
    price = cityobj.getPrice()
    if cityobj.getGroup() in gamevalue.buyable and cityobj.getOwner() == "Banker":
        # ask to buy
        tokenobj.printInfo()
        choice = input(f'[{tokenobj.getName():6}] do you wish to buy {cityobj.getName():_>10} for {price} <y/n>:')
        if choice not in ('y', 'Y'): return
        if tokenobj.checkBalance(price):
            tokenobj.debit(price)
            tokenobj.addWealth(price)
            cityobj.setOwner(pname)
        else: print(f'[{tokenobj.getName():6}]', 'insufficient balance')
        # tokenobj.printInfo()
    elif cityobj.getGroup() == "Tax":
        # calculate tax
        pass
    elif cityobj.getOwner() == pname:
        print(f'[{tokenobj.getName():6}]', 'its my city')
    else:
        # pay rent to city owner
        pass
    boardobj.printAllCities()
    