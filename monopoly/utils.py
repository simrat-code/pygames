
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
        # credit round finish bonus
        tokenobj.credit( boardobj.getCellObject(0).getRent() )
        # print(f'[{tokenobj.getName():6}] points credited')
        tokenobj.printInfo()
    print(f'[{tokenobj.getName():6}] dice: {tokenobj.getDice()} | reaches', cityobj.getBelong(), f'| pos {pos:02}' )
    return pos, cityobj

def play(tokenobj, boardobj):
    """ Return city-owner and rent
    if current play step-on others property.
    else it will return (None, 0)
    inside 'runme.py', bank will credit the points to owner
    since 'tokenobj' points to current player and do not have owner's object to call credit()
    currently, Card.owner is string type and not object of Player-class
    """
    if not isinstance(tokenobj, Player): return None, 0
    if not isinstance(boardobj, Board): return None, 0
    pname = tokenobj.getName()
    pos, cityobj = makeMove(tokenobj, boardobj)
    price = cityobj.getPrice()
    if cityobj.getGroup() in gamevalue.buyable and cityobj.getOwner() == "Banker":
        # ask to buy
        tokenobj.printInfo()
        choice = input(f'[{tokenobj.getName():6}] buy {cityobj.getName():_>10} for {price} <y/n>: ')
        if choice not in ('y', 'Y'): return None, 0
        if tokenobj.checkBalance(price):
            tokenobj.debit(price)
            tokenobj.addWealth(price)
            tokenobj.addOwned(int(pos))
            cityobj.setOwner(pname)
        else: print(f'[{tokenobj.getName():6}]', 'insufficient balance')
        boardobj.printAllCities()

    elif cityobj.getGroup() == "Tax":
        # calculate tax
        tax = cityobj.getRent(tokenobj)
        tokenobj.debit(tax)
    
    elif cityobj.getOwner() == pname:
        print(f'[{tokenobj.getName():6}]', 'its my city')
    
    else:
        # pay rent to city owner
        print(f'[{tokenobj.getName():6}] paying {cityobj.getRent()} to {cityobj.getOwner()}')
        return payRent(tokenobj, cityobj, boardobj)
    return None, 0
    
def payRent(tokenobj, cityobj, boardobj):
    if not isinstance(tokenobj, Player) or not isinstance(cityobj, Card):
        return None, 0
    rent = cityobj.getRent(tokenobj)
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
            saleProperty(tokenobj, boardobj)
    
    tokenobj.debit(rent)
    return cityobj.getOwner(), rent
    # return None, 0

def saleProperty(tokenobj, boardobj):
    if not isinstance(tokenobj, Player) or not isinstance(boardobj, Board): return
    for index in tokenobj.parseOwnedGen():
        boardobj.printCitySaleInfo(index)
    try:
        choice = int(input('enter city index to sale: '))
        if not tokenobj.isOwned(choice): return
        tokenobj.credit( boardobj.saleCard(choice))
        tokenobj.delOwned(choice)
    except:
        pass