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
    def insertNodo(self, node):
        if self.root is None:
            self.root = node

    def getRaizData(self):
        n = self.root.getData()
        return n