
import xml.etree.ElementTree as ET
import gamevalue

from card import Card, City
from card import Corp
from card import Banker
from card import Tax

class Board():
    def __init__(self, confname):
        self.conf = confname
        self.db = {}        # {0:"Start", 1:"Goa", ...}
        # self.citydb = {}    # {"Start":{...}, "Goa":{...}, ...}

    def _prepareDB(self, elem):
        block = {}     
        if elem.tag == "cell":
            id = elem.find("id")
            group = elem.find("group")
            if id != None and group != None:
                # 'id' and 'group' tags found and append to 'db'
                for child in elem:
                    block[child.tag] = child.text
                self.db[int(id.text)] = eval(group.text)(**block)

    def parseConfig(self):        
        for event, elem in ET.iterparse(self.conf, events=("end",)):
            self._prepareDB(elem)
        print(f'{len(self.db)}')

    def printCityGen(self, color, endchar=" "):
        print('-'*14 + f' {color} ' + '-'*(17 - len(color)), end=endchar )
        yield
        if color not in gamevalue.cardcolor:
            return
        for id, obj in self.db.items():
            if obj.getGroup() in ("City", "Corp") and obj.getColor() == color:
                print(obj.getSummary(), end=endchar)
                yield

    def printCity(self, color):
        for _ in self.printCityGen(color, '\n'):
            pass

    def printCitySaleInfo(self, index):
        print(self.db[index].getSaleInfo())

    def printAllCities(self):
        # used less intelligent way to print city detail in tabular format
        # but its working ;P
        obj = []
        for i, color in enumerate(gamevalue.cardcolor):
            obj.append( self.printCityGen(color, " | ") )
        for _ in range(6):
            next(obj[0])
            next(obj[1])
            next(obj[2])
            print('')
        for _ in range(6):
            next(obj[4])
            next(obj[3])
            print('')
        next(obj[4])
        print('')

    # def fetchCity(self, cityname): return self.citydb[cityname]

    def getCellObject(self, index): return self.db[index]

    def setOwner(self, index, pname): self.db[index].setOwner(pname)

    def printBoard(self):
        pass
    
    def saleCard(self, index):
        """ Return property value """
        # set owner back to "Banker"
        obj = self.db[index]
        if not isinstance(obj, Card): return 0
        amount = 1000 * (obj.getBuildings() - 1)
        amount += obj.getPrice()
        obj.reset()
        return amount

# -- END --