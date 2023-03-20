###############################################
# Created by iiSeymour
# Changed by Mandeep Singh
# Changed date: 03/21/2019
# Licensce: free to use
#############################################

from flask import Flask, render_template
from altair import Chart, X, Y, Axis, Data, DataFormat
import altair as alt
import pandas as pd

# load a simple dataset as a pandas DataFrame
from vega_datasets import data
cars = data.cars()
electricity = data.iowa_electricity()
barley_yield = data.barley()

app = Flask(__name__)

##########################
# Flask routes
##########################
# render index.html home page
@app.route("/")
def index():
    return render_template('index.html')

# Creates graph for IOWA electricity consumption
@app.route("/data/electricity")
def electricity_demo():

    chart = Chart(
        data=electricity, height=700, width=700).mark_area(tooltip=True).encode(
            x="year:T", y="net_generation:Q", color="source:N").interactive()
    return chart.to_json()

@app.route("/data/income")
def income_demo():
    data = pd.read_csv('data/owid-co2-data.csv')
    income_level_countries = data[data['country'].isin(['Low-income countries', 'Lower-middle-income countries','Upper-middle-income countries','High-income countries'])]
    income_level_countries = income_level_countries.query('year>=1990')[['country','year','population','total_ghg','gdp']]
    
    chart1= Chart(income_level_countries, title='Annual Greenhouse Gas (Million Tonnes) Per Income Level').mark_area(opacity=0.7).encode(
    x=alt.X('year:O',title='Year'),
    y=alt.Y('total_ghg:Q',title='Million Tonnes'),
    color = alt.Color('country',title='Country'),
    tooltip=[alt.Tooltip('year:O',title='Year'),
            alt.Tooltip('total_ghg:Q',title='Million Tonnes'),
             alt.Tooltip('country:N',title='Income Level')]
        )
    return chart1.to_json()


if __name__ == "__main__":
    app.run(debug=True)