from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def Index():
    return render_template('home.html')

@app.route('/about')
def About():
    return render_template('about.html')
    
""" Por defecto Flask inicia en localhost:5000 """
if __name__ == '__main__':
    app.run(debug=True)