
class Player(object):
    def __init__(self, name):
        self.name = name
        self.owned = []
        self.income = 12000
        self.wealth = 0
        self.counter = 0
        self.pos = 0        # initial position at "Start"

    def printInfo(self):
        print(f'balance for {self.name:x>5} is {self.income} with {self.wealth}')

    def debit(self, val): self.income -= val

    def credit(self, val): self.income += val

    def addWealth(self, val): self.wealth += val

    def getName(self): return self.name

    def getIncome(self): return self.income

    def getWealth(self): return self.wealth

    def getPosition(self): return self.pos

    def incrPosition(self, val): self.pos = (self.pos + val) % 32

    def checkBalance(self, val): return self.income > val