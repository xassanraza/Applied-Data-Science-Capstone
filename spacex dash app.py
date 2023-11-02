# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)
dropdown_options=[{'label': 'All Sites', 'value': 'ALL'},
  {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
  {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'},
  {'label':'KSC LC-39A','value':'KSC LC-39A'},
  {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'}]


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options = dropdown_options,
                                value = 'ALL',
                                placeholder='Sites',
                                searchable = True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000,
                                marks={0: '0',100: '100',10000:'10000'},
                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
'''
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(data, values='class', 
        names='pie chart names', 
        title='title')
        return fig
    else:
        # return the outcomes piechart for a selected site
'''

@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # If ALL sites are selected, calculate total success launches
        total_success = len(spacex_df[spacex_df['class'] == 1])
        total_failures = len(spacex_df[spacex_df['class'] == 0])
        labels = ['Success', 'Failure']
        values = [total_success, total_failures]
    else:
        # If a specific site is selected, filter the dataframe and calculate success and failure counts
        site_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        success_count = len(site_df[site_df['class'] == 1])
        failure_count = len(site_df[site_df['class'] == 0])
        labels = ['Success', 'Failure']
        values = [success_count, failure_count]

    # Create and return the pie chart
    fig = px.pie(
        values=values,
        names=labels,
        title=f'Success vs Failure for {selected_site}' if selected_site != 'ALL' else 'Total Success vs Failure'
    )
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'ALL':
        # If ALL sites are selected, render a scatter plot for all launch sites
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Payload Mass vs. Success for All Sites')
    else:
        # If a specific site is selected, filter the DataFrame and render the scatter chart
        site_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        filtered_df = site_df[(site_df['Payload Mass (kg)'] >= payload_range[0]) & (site_df['Payload Mass (kg)'] <= payload_range[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title=f'Payload Mass vs. Success for {selected_site}')
    
    return fig
# Run the app
if __name__ == '__main__':
    app.run_server()
