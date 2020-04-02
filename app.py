from flask import Flask, render_template
from scrap import table


app = Flask(__name__)


name = 'james gitua'


@app.route('/')
def dashboard():
    data = table()
    return render_template('base.html', data=data)
