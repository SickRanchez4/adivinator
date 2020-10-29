class Arbol:
    def __init__(self):
        self.root=None

    def __str__(self):  # Imprimir algun recorrido
        return str(self.root)
    
#   GETTERS
    def getRoot(self):
        return self.root

#   SETTERS
    def setRoot(self, node):
        self.root = node

#   METODOS
    def insertAnimal(self, name, diff, ind):
        animal = self.getRoot()
        self.setRoot(diff)
        if ind == "NO":
            self.getRoot().setLeft(animal)
            self.getRoot().setRight(name)
        else:
            self.getRoot().setRight(animal)
            self.getRoot().setLeft(name)

    def recorrido(self):
        while self.getRoot().getLeft() != None:
            if si(arbol.carga + "? "):
                arbol = arbol.izquierda
            else:
                arbol = arbol.derecha

    def getRaizData(self):
        n = self.root.getData()
        return n