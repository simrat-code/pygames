
import xml.etree.ElementTree as ET
import gamevalue

class Board():
    def __init__(self, confname):
        self.conf = confname
        self.db = {}        # {0:"Start", 1:"Goa", ...}
        self.citydb = {}    # {"Start":{...}, "Goa":{...}, ...}

    def _prepareDB(self, elem):
        block = {'owner': 'Banker'}     # initially set owner of each card as 'Banker'
        if elem.tag == "cell":
            id = elem.find("id")
            name = elem.find("name")
            if id != None and name != None:
                # both tag exist and found
                # append to 'db'
                self.db[int(id.text)] = name.text
            # add all block data to citydb
            for child in elem:
                block[child.tag] = child.text
            self.citydb[name.text] = block

    def parseConfig(self):        
        for event, elem in ET.iterparse(self.conf, events=("end",)):
            self._prepareDB(elem)
        print(f'{len(self.db)}')

    def printCity(self, color):
        print('-'*7 + f' {color} ' + '-'*(16 - len(color)) )
        if color not in gamevalue.cardcolor:
            return
        for name, ele in self.citydb.items():
            if ele['type'] in ("City", "Corp") and ele['color'] == color:
                # since 'rent' is None currently
                # format string expect string-object and not NoneType
                # so converting None to empty string
                print(f'{ele["name"]:12} {ele["price"]:>5} {str(ele["rent"]):>5} {ele["owner"]:8}')

    def printAllCities(self):
        for c in gamevalue.cardcolor:
            self.printCity(c)

    def fetchCity(self, cityname): return self.citydb[cityname]

    def getCellName(self, val): return self.db[val]

    def setOwner(self, cityname, pname): self.citydb[cityname]["owner"] = pname

    def printBoard(self):
        pass
    

# -- END --