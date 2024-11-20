# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import numpy as np
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_sites = spacex_df['Launch Site'].unique()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),

                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=np.insert(launch_sites, 0, "All"),
                                    value="All"
                                ),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(
                                    id='success-pie-chart'
                                )),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=min_payload,
                                    max=max_payload,
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output("success-pie-chart", "figure"),
    Input("site-dropdown", "value"),
)
def generate_pie_chart(launch_site):
    df = spacex_df if launch_site == "All" else spacex_df[spacex_df["Launch Site"] == launch_site]
    fig = px.pie(df, names="class")
    return fig
    

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output("success-payload-scatter-chart", "figure"),
    Input("site-dropdown", "value"),
    Input("payload-slider", "value"),
)
def generate_scatter_chart(launch_site, payload):
    print("calculateting scatter chart", launch_site, payload)
    if(payload == None):
        df = spacex_df
    elif launch_site == "All":
        df = spacex_df.where(
            (spacex_df["Payload Mass (kg)"] > payload[0]) & 
            (spacex_df["Payload Mass (kg)"] < payload[1]))
    else:
        df = spacex_df.where(
            (spacex_df["Launch Site"] == launch_site) & 
            (spacex_df["Payload Mass (kg)"] > payload[0]) &
            (spacex_df["Payload Mass (kg)"] < payload[1]))
    fig = px.scatter(
        df, 
        x="Payload Mass (kg)", 
        y="class",
        color="Booster Version Category"
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()