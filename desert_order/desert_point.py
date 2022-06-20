



class DesertPoint:
    def __init__(self, x, y):
        self.x = x 
        self.y = y 

    def __str__(self):
        return "{} {}".format(self.x, self.y)

    def __getitem__(self, key):
        if key == 'x': return self.x 
        elif key == 'y': return self.y 
        else: KeyError("Execption: passed key does not exist in DesertPoint object")