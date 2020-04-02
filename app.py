import numpy as np
from flask import Flask, render_template
import plotly
import plotly.express as px
import pandas as pd
from scrap import table
import json


app = Flask(__name__)

iso_alpha = pd.read_csv('iso_codes')
data = table()

# fig.write_html('index.html', full_html=True)


def create_map(group):
    df_merge_col = pd.merge(data, iso_alpha, on='country')

    fig = px.choropleth(df_merge_col, locations="iso_alpha", color=group,
                        hover_name="country", title='confirmed covid19 cases', projection='natural earth',
                        hover_data=['recovered', 'serious', 'deceased'])

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


@app.route('/')
def dashboard():
    jsonmap = create_map(group='confirmed')
    return render_template('confirmed.html', jsonmap=jsonmap)


@app.route('/serious/')
def serious():
    jsonmap = create_map(group='serious')
    return render_template('serious.html', jsonmap=jsonmap)


@app.route('/deceased/')
def deceased():
    jsonmap = create_map(group='deceased')
    return render_template('deceased.html', jsonmap=jsonmap)

@app.route('/recovered')
def recovered():
    jsonmap = create_map(group='recovered')
    return render_template('recovered.html', jsonmap=jsonmap)
