
from card import Card
import random
import gamevalue

from player import Player
from board import Board

def rolldice():
    return random.randint(1, 6)

def makeMove(tokenobj, boardobj):
    """ Returns pos and cityobj """
    oldpos = tokenobj.getPosition()
    pos = tokenobj.incrPosition(rolldice())
    cityobj = boardobj.getCellObject(pos)    
    if pos - oldpos <= 0:
        # credit salary
        tokenobj.credit( boardobj.getCellObject(0).getRent() )
        print(f'[{tokenobj.getName():6}]', 'points credited')
        tokenobj.printInfo()
    print(f'[{tokenobj.getName():6}]', f'dice roll: {tokenobj.getDice()} | reaches', cityobj.getBelong() )
    return pos, cityobj

def play(tokenobj, boardobj):
    """ Return city-owner and rent
    if current play step-on others property.
    else it will return (None, 0)
    """
    if not isinstance(tokenobj, Player): return None, 0
    if not isinstance(boardobj, Board): return None, 0
    pname = tokenobj.getName()
    pos, cityobj = makeMove(tokenobj, boardobj)
    price = cityobj.getPrice()
    if cityobj.getGroup() in gamevalue.buyable and cityobj.getOwner() == "Banker":
        # ask to buy
        tokenobj.printInfo()
        choice = input(f'[{tokenobj.getName():6}] do you wish to buy {cityobj.getName():_>10} for {price} <y/n>:')
        if choice not in ('y', 'Y'): return None, 0
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
        # rent = cityobj.getRent()
        # print(f'[{tokenobj.getName():6}] paying {rent} to {cityobj.getOwner()}')
        # if tokenobj.checkBalance(rent):
        #     tokenobj.debit(rent)
        # else:
        #     # need to sell some property
        #     pass
        # return cityobj.getOwner(), rent
        return payRent(tokenobj, cityobj)
    boardobj.printAllCities()
    return None, 0
    
def payRent(tokenobj, cityobj):
    if not isinstance(tokenobj, Player) or not isinstance(cityobj, Card):
        return None, 0
    rent = cityobj.getRent()
    while not tokenobj.checkBalance(rent):
        # not sufficient balance, then sell property
        # IF no property left, declare Bankrupt
        # and whatever income is left will be paid against standing rent.
        if tokenobj.getWealth() == 0:
            print(f'[{tokenobj.getName():6}] has become bankrupt')
            rent = tokenobj.getIncome()
            tokenobj.declareBankrupt()
            break
        else:
            saleProperty(tokenobj)
    
    tokenobj.debit(rent)
    return cityobj.getOwner(), rent
    # return None, 0

def saleProperty(tokenobj):
    if not isinstance(tokenobj, Player): return