from flask import Flask, render_template
from static.game import Gamin

app = Flask(__name__)

@app.route('/')
def Index():
    Gamin()
    return render_template('home.html')

@app.route('/about')
def About():
    return render_template('about.html')

""" @app.route('/game')
def Game():
    Gamin()
    return 0 """


""" Por defecto Flask inicia en localhost:5000 """
if __name__ == '__main__':
    app.run(debug=True)
    