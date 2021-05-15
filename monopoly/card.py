
class Card():
    def __init__(self, name, price, rent, isbuidable = False):
        self.name = name
        self.price = price * 1
        self.rent = rent * 1
        self.isbuildable = isbuidable
        self.buildings = 1.0

    def calculateRent(self, dice):
        if not isinstance(dice, int):
            print("invalid type to calculateRent")
            return self.rent
        return self.rent * self.buildings

    def addBuilding(self):
        if self.buildings < 3.0:
            self.buildings += 0.5