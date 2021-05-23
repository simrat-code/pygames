
from typing import Counter


class Player(object):
    def __init__(self, name):
        self.name = name
        self.owned = []
        self.income = 12000
        self.wealth = 0
        self.trip = 0
        self.pos = 0        # initial position at "Start"
        self.dice = 0
        self.active = True

    def printInfo(self):
        print(f'[{self.name:6}] balance is {self.income} with wealth {self.wealth}')

    def debit(self, val): self.income -= val
    def credit(self, val): self.income += val
    def addWealth(self, val): self.wealth += val
    def checkBalance(self, val): return self.income > val
    def isActive(self): return self.active
    def declareBankrupt(self): self.active = False

    def getName(self): return self.name
    def getPosition(self): return self.pos
    def getDice(self): return self.dice
    def getIncome(self): return self.income
    def getWealth(self): return self.wealth

    def incrPosition(self, val): 
        self.dice = val
        if (self.pos + val >= 32): self.trip += 1
        self.pos = (self.pos + val) % 32
        return self.pos
