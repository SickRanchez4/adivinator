from static.nodo import Nodo
from static.arbol import Arbol

def Gamin():
    print('\n--> JUGANDO <--\n')
    playin = True

    node = Nodo()
    node.setData('Perro')
    Tree = Arbol()
    Tree.setRoot(node)
    a = Tree.getRaizData()
    return print(a)
