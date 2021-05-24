
from player import Player

class Card():
    def __init__(self, id, name, price, rent, group, color, isbuildable = False):
        self.celldb = {
            'id' : id,
            'name' : name,
            'price' : int(price),
            'rent' : int(rent) if rent else 100,
            'group' : group,
            'color' : color,
            'isbuildable' : isbuildable,
            'buildings' : 1,
            'owner' : None,
            'ownerobj' : None
        }

    def getOwnerObj(self): return self.celldb['ownerobj']
    def getOwnerName(self): return self.celldb['owner']
    def getName(self): return self.celldb['name']
    def getPrice(self): return self.celldb['price']
    def getRent(self, obj=None): return self.celldb['rent'] * self.celldb['buildings']
    def getGroup(self): return self.celldb['group']
    def getColor(self): return self.celldb['color']
    def getBuildings(self): return self.celldb['buildings']
    def isBuildable(self): return self.celldb['isbuildable']

    def getSummary(self): return '{name:12} {price:>5} {rent:>5} {owner:8}'.format(**self.celldb)
    def getBelong(self): return '{name:_>10} belongs to {owner:>6} with rent {rent}'.format(**self.celldb)
    def getSaleInfo(self): return '{id:>2} {name:12} {price:>5} {rent:>5} {buildings}'.format(**self.celldb)

    def setOwnerObj(self, obj): 
        self.celldb['ownerobj'] = obj
        self.celldb['owner'] = obj.getName()
        
    def reset(self, ownerobj):
        self.celldb['buildings'] = 1
        self.celldb['ownerobj'] = ownerobj
        self.celldb['owner'] = ownerobj.getName()
        

class City(Card):
    def __init__(self, id, name, price, rent, group, color):
        super().__init__(id, name, price, rent, group, color, True)

    def addBuilding(self):
        if self.buildings <= 4:
            self.buildings += 1


class Corp(Card):
    def __init__(self, id, name, price, rent, group, color):
        super().__init__(id, name, price, rent, group, color, isbuildable=False)

    def getRent(self, obj):
        """ multiple dice with rent """
        if not isinstance(obj, Player): return super().getRent()
        return self.celldb['rent'] * obj.getDice()


class Banker(Card):
    def __init__(self, id, name, price, rent, group, color=None):
        super().__init__(id, name, price, rent, group, color, isbuildable=False)



class Tax (Card):
    def __init__(self, id, name, price, rent, group, color=None):
        super().__init__(id, name, price, rent, group, color, isbuildable=False)

    def getRent(self, playerobj):
        """ Deduct multiple of 100 """
        val = 0
        if (self.celldb['name'] == "IncomeTax"):
            val = int(float(playerobj.getIncome()) * float(self.celldb['rent'])/100.0 )
        elif (self.celldb['name'] == "WealthTax"):
            val = int(float(playerobj.getWealth()) * float(self.celldb['rent'])/100.0 )
        else:
            pass    # no tax
        return 0 if val < 100 else val - (val % 100)


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

    