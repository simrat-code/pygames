
import xml.etree.ElementTree as ET
import gamevalue

class Board():
    def __init__(self, confname):
        self.conf = confname
        self.db = {}        # {0:"Start", 1:"Goa", ...}
        self.citydb = {}    # {"Start":{...}, "Goa":{...}, ...}

    def parseConfig(self):        
        for event, elem in ET.iterparse(self.conf, events=("end",)):
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
                self.citydb[name] = block
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

    

# -- END --