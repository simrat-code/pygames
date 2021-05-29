
from typing import Counter
from utils import highlighter


class Player(object):
    def __init__(self, name):
        self.name = name
        self.owned = []
        self.income = 12000
        self.wealth = 0
        self.trip = 1
        self.pos = 0        # initial position at "Start"
        self.dice = 0
        self.active = True

    def printInfo(self):
        print(
            highlighter(
                f'[{self.name:6}] balance {self.income} property {self.wealth}'
            )
        )

    def debit(self, val): 
        self.income -= val
        print(
            highlighter(
                f'[{self.name:6}] debit  {val:03}, balance {self.income}'
            )
        )

    def credit(self, val): 
        self.income += val
        print(
            highlighter(
                f'[{self.name:6}] credit {val:03}, balance {self.income}'
            )
        )
    
    def addWealth(self, val): self.wealth += val
    def addOwned(self, index): self.owned.append(index)
    def delOwned(self, index): self.owned.remove(index)
    def isOwned(self, index): return index in self.owned
    def checkBalance(self, val): return self.income >= val
    def isActive(self): return self.active
    def declareBankrupt(self): self.active = False

    def getName(self): return self.name
    def getPosition(self): return self.pos
    def getDice(self): return self.dice
    def getTrip(self): return self.trip
    def getIncome(self): return self.income
    def getWealth(self): return self.wealth

    def parseOwnedGen(self): 
        for val in self.owned: yield val 
    
    def incrPosition(self, val): 
        self.dice = val
        if (self.pos + val >= 32): self.trip += 1
        self.pos = (self.pos + val) % 32
        return self.pos
