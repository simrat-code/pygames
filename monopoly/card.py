
class Card():
    def __init__(self, id, name, price, rent, group, color, isbuildable = False):
        self.name = name
        self.price = price * 1
        self.rent = rent * 1
        self.color = color
        self.isbuildable = isbuildable
        self.buildings = 1.0

    # def setBuildable(self, val=True): self.isbuildable = val

    def calculateRent(self, dice):
        if not isinstance(dice, int):
            print("invalid type to calculateRent")
            return self.rent
        if self.isbuildable:
            # for City
            return self.rent * self.buildings
        else:
            # for Corp
            return dice * self.rent
  

class City(Card):
    def __init__(self, id, name, price, rent, group, color):
        super().__init__(id, name, price, rent, group, color, True)
        # self.setBuildable()

    def addBuilding(self):
        if self.buildings < 3.0:
            self.buildings += 0.5


class Corp(Card):
    def __init__(self, name, price, rent):
        super().__init__(name, price, rent, isbuildable=False)


class Banker(Card):
    def __init__(self, name, price, rent, isbuildable):
        super().__init__(name, price, rent, isbuildable=False)

    def calculateRent(self, dice):
        return self.rent

if __name__ == "__main__":
    var = 'this {name} has {color} color'
    block = {
        'id': 1,
        'name': 'Goa',
        'price': 3000,
        'rent': 100,
        'group': 'City',
        'color': 'Green'
    }
    print(var.format(**block))
    cityobj = City(**block)
    # print(cityobj.calculateRent(4))

    