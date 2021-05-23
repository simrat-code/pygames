
class Card():
    def __init__(self, id, name, price, rent, group, color, isbuildable = False):
        self.celldb = {
            'name' : name,
            'price' : int(price),
            'rent' : int(rent) if rent else 100,
            'group' : group,
            'color' : color,
            'isbuildable' : isbuildable,
            'buildings' : 1,
            'owner' : "Banker"
        }

    def getOwner(self): return self.celldb['owner']
    def getName(self): return self.celldb['name']
    def getPrice(self): return self.celldb['price']
    def getRent(self): return self.celldb['rent'] * self.celldb['buildings']
    def getGroup(self): return self.celldb['group']
    def getColor(self): return self.celldb['color']
    def getBuildings(self): return self.celldb['buildings']
    def isBuildable(self): return self.celldb['isbuildable']

    def getSummary(self): return '{name:12} {price:>5} {rent:>5} {owner:8}'.format(**self.celldb)
    def getBelong(self): return '{name:_>10} belongs to {owner:>6} with rent {rent}'.format(**self.celldb)
    def getSaleInfo(self): return '{id:>2} {name:12} {price:>5} {rent:>5} {buildings}'.format(**self.celldb)

    def setOwner(self, owner): self.celldb['owner'] = owner
    def reset(self):
        self.celldb['buildings'] = 1
        self.celldb['owner'] = "Banker"
        

class City(Card):
    def __init__(self, id, name, price, rent, group, color):
        super().__init__(id, name, price, rent, group, color, True)

    def addBuilding(self):
        if self.buildings <= 4:
            self.buildings += 1


class Corp(Card):
    def __init__(self, id, name, price, rent, group, color):
        super().__init__(id, name, price, rent, group, color, isbuildable=False)


class Banker(Card):
    def __init__(self, id, name, price, rent, group, color=None):
        super().__init__(id, name, price, rent, group, color, isbuildable=False)



class Tax (Card):
    def __init__(self, id, name, price, rent, group, color=None):
        super().__init__(id, name, price, rent, group, color, isbuildable=False)

    def getRent(self, dice, playerobj):
        if (self.name == "IncomeTax"):
            val = float(playerobj.getIncome()) * 0.1
            return int(val)
        elif (self.name == "WealthTax"):
            val = float(playerobj.getWealth()) * 0.1
            return int(val)
        else:
            return 100


if __name__ == "__main__":
    var = 'this {name} has {color} color'
    block = {
        'id': 1,
        'name': 'Chandigarh',
        'price': 4000,
        'rent': 300,
        'group': 'City',
        'color': 'Green'
    }
    print(var.format(**block))
    cityobj = City(**block)
    print(cityobj.getRent())
    print(cityobj.getSummary())

    