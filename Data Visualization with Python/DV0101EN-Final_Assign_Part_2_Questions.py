import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Dropdown menu options
dropdown_options = [
    {'label': 'Yearly Sales Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
year_list = [i for i in range(1980, 2024, 1)]

# Layout of the app
app.layout = html.Div([
    html.H1("Automobile Sales Dashboard"),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Yearly Statistics'
        )
    ]),
    html.Div(dcc.Dropdown(
        id='select-year',
        options=[{'label': i, 'value': i} for i in year_list],
        value=1980
    )),
    html.Div(id='output-container', className='container-output')
])

@app.callback(
    Output('select-year', 'style'),
    Input('dropdown-statistics', 'value')
)
def update_input_visibility(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'),
     Input('select-year', 'value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]
        
        fig1 = px.line(recession_data, x="Year", y="Automobile_Sales", title="Automobile Sales During Recession")
        fig2 = px.bar(recession_data, x="Vehicle_Type", y="Automobile_Sales", title="Sales by Vehicle Type During Recession")
        fig3 = px.pie(recession_data, names="Vehicle_Type", values="Automobile_Sales", title="Sales Distribution by Vehicle Type During Recession")
        fig4 = px.bar(recession_data, x="Year", y="unemployment_rate", title="Unemployment Rate During Recession")
        
        return [
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2),
            dcc.Graph(figure=fig3),
            dcc.Graph(figure=fig4)
        ]

    elif selected_statistics == 'Yearly Statistics' and input_year:
        yearly_data = data[data['Year'] == input_year]
        
        fig1 = px.line(data, x="Year", y="Automobile_Sales", title=f"Yearly Automobile Sales")
        fig2 = px.bar(yearly_data, x="Month", y="Automobile_Sales", title=f"Monthly Sales in {input_year}")
        fig3 = px.bar(yearly_data, x="Vehicle_Type", y="Automobile_Sales", title=f"Sales by Vehicle Type in {input_year}")
        fig4 = px.pie(yearly_data, names="Vehicle_Type", values="Advertising_Expenditure", title=f"Advertisement Expenditure by Vehicle Type in {input_year}")
        
        return [
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2),
            dcc.Graph(figure=fig3),
            dcc.Graph(figure=fig4)
        ]

    else:
        return None

if __name__ == '__main__':
    app.run_server(debug=True)