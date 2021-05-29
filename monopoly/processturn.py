
import gamevalue

from player import Player
from board import Board
from card import Card
from utils import rolldice

def makeMove(tokenobj, boardobj):
    """ Returns pos and Card """
    oldpos = tokenobj.getPosition()
    pos = tokenobj.incrPosition(rolldice())
    cityobj = boardobj.getCellObject(pos)    
    if pos - oldpos <= 0:
        # credit round finish bonus
        tokenobj.credit( boardobj.getCellObject(0).getRent() )
    print(f'[{tokenobj.getNameC():6}] dice: {tokenobj.getDice()} | reaches', cityobj.getBelong(), f'| pos {pos:02}' )
    return pos, cityobj

def play(tokenobj, boardobj):
    """
    if current player step-on others property, Debit rent from current player and
    credit it to city's owner
    
    since 'tokenobj' points to current player and 
    cityobj.getOwnerObj() will get owner's object
    """
    if not isinstance(tokenobj, Player): return 
    if not isinstance(boardobj, Board): return 
    boardobj.printAllCities()
    print('')
    pos, cityobj = makeMove(tokenobj, boardobj)
    if not isinstance(cityobj, Card): return 
    price = cityobj.getPrice()
    
    if cityobj.getName() == "Start":
        # points already credited, do nothing
        pass
    
    elif cityobj.getGroup() in gamevalue.buyable and cityobj.getOwnerName() == "Banker":
        # ask to buy
        tokenobj.printInfo()
        choice = input(f'[{tokenobj.getNameC():6}] buy {cityobj.getName():^10} for {price} <y/n>: ')
        if choice not in ('y', 'Y'): return 
        if tokenobj.checkBalance(price):
            tokenobj.debit(price)
            tokenobj.addWealth(price)
            tokenobj.addOwned(int(pos))
            cityobj.setOwnerObj(tokenobj)
        else: print(f'[{tokenobj.getNameC():6}]', 'insufficient balance')

    elif cityobj.getGroup() == "Tax":
        # calculate tax
        tax = cityobj.getRent(tokenobj)
        tokenobj.debit(tax)
    
    elif cityobj.getOwnerObj() is tokenobj:
        print(f'[{tokenobj.getNameC():6}]', 'its my city')
    
    else:
        # pay rent to city owner
        payRent(tokenobj, cityobj, boardobj)
    
def payRent(tokenobj, cityobj, boardobj):
    if not isinstance(tokenobj, Player) or not isinstance(cityobj, Card):
        return 
    rent = cityobj.getRent(tokenobj)
    while not tokenobj.checkBalance(rent):
        # not sufficient balance, then sell property
        # IF no property left, declare Bankrupt
        # and whatever income is left will be paid against standing rent.
        if tokenobj.getWealth() == 0:
            print(f'[{tokenobj.getNameC():6}] has become bankrupt')
            rent = tokenobj.getIncome()
            tokenobj.declareBankrupt()
            break
        else:
            saleProperty(tokenobj, boardobj)
    # debit fro current player
    # credit to city owner
    tokenobj.debit(rent)
    cityobj.getOwnerObj().credit(rent)
    return

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