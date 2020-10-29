class Nodo:
    def __init__(self):
        self.data = None
        self.left = None
        self.right = None

    def __str__(self):
        return str(self.data)

#   GETTERS
    def getData(self):
        return self.data

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

#   SETTERS
    def setData(self, d):
        self.data = d
    
    def setLeft(self, l):
        self.left = l
    
    def setRight(self, r):
        self.right = r

#   MÉTODOS
    def esHoja(self):
        if self.getRight() is None and self.getLeft() is None:
            return True
        else:
            return False