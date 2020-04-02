from flask import Flask, render_template
from scrap import data


app = Flask(__name__)


name = 'james gitua'
@app.route('/')
def dashboard():
    return render_template('base.html', data=data)
    # return html