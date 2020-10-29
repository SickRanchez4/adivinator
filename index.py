from flask import Flask, render_template, request, redirect
from static.nodo import Nodo
from static.arbol import Arbol

#   Game Enviroment
node = Nodo()
node.setData('Perro')

arb = Arbol()
arb.setRoot(node)


# Flask
app = Flask(__name__)

@app.route('/')
def Index():
    return render_template('home.html', tree = arb)

@app.route('/about')
def About():
    return render_template('about.html')

@app.route('/newanimal', methods=['POST'])
def Newanimal():
    new_name = request.form['newname']
    new_diff = request.form['newdiff']
    indicador = request.form['newresp']
    name = Nodo()
    preg = Nodo() #se hace raiz
    name.setData(new_name)
    preg.setData(new_diff)
    arb.insertAnimal(name, preg, indicador)
    print(arb)
    return redirect('/')

@app.route('/goLeft')
def goLeft():
    L = arb.getRoot().getLeft()
    arb.setRoot(L)
    return redirect('/')

@app.route('/goRight')
def goRight():
    R = arb.getRoot().getRight()
    arb.setRoot(R)
    return redirect('/')

""" @app.route('/move')
def move():
    ans = request.form['resp']
    if ans == 'SI':
        R = arb.getRoot().getRight()
        arb.setRoot(R)
    else
    return redirect('/') """




""" Por defecto Flask inicia en localhost:5000 """
if __name__ == '__main__':
    app.run(debug=True)
    