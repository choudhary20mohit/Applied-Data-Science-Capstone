# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

options = [
    {'label': 'All Sites', 'value': 'ALL'},
    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}]

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=options,
                                    value='ALL',
                                    placeholder='Select a Launch Site',
                                    searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0, 
                                    max=10000,
                                    step=1000,
                                    value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown',component_property='value'))

# Function decorator to specify function input and output
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total success launch by site')
        return fig
    
    elif entered_site == 'CCAFS LC-40':
        CCAFS_LC_40_df = filtered_df[filtered_df['Launch Site']=='CCAFS LC-40']
        CCAFS_LC_40= CCAFS_LC_40_df.groupby('class').count().reset_index()
        fig = px.pie(CCAFS_LC_40, values='Launch Site',
        names='class',
        title='Total success launch for site CCAFS LC-40')
        return fig        

    elif entered_site == 'VAFB SLC-4E':
        VAFB_SLC_4E_df = filtered_df[filtered_df['Launch Site']=='VAFB SLC-4E']
        VAFB_SLC_4E= VAFB_SLC_4E_df.groupby('class').count().reset_index()
        fig = px.pie(VAFB_SLC_4E, values='Launch Site', 
        names='class', 
        title='Total success launch for site VAFB SLC-4E')
        return fig

    elif entered_site == 'KSC LC-39A':
        KSC_LC_9A_df = filtered_df[filtered_df['Launch Site']=='KSC LC-39A']
        KSC_LC_9A= KSC_LC_9A_df.groupby('class').count().reset_index()
        fig = px.pie(KSC_LC_9A, values='Launch Site', 
        names='class', 
        title='Total success launch for site KSC LC-39A')
        return fig

    else:
        # return the outcomes piechart for a selected site
        CCAFS_SLC_40_df == filtered_df[filtered_df['Launch Site']=='CCAFS SLC-40']
        CCAFS_SLC_40= CCAFS_SLC_40_df.groupby('class').count().reset_index()
        fig = px.pie(CCAFS_SLC_40, values='Launch Site', 
        names='class', 
        title='Total success launch for site CCAFS SLC-40')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), 
    Input(component_id="payload-slider", component_property="value")])

def update_output(entered_site, value1):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        All_df = filtered_df[(filtered_df['Payload Mass (kg)']>=value1[0])&(filtered_df['Payload Mass (kg)']<=value1[1])]
        fig = px.scatter(All_df, x="Payload Mass (kg)", y="class", color='Booster Version Category')
        return fig     
    
    elif entered_site == 'CCAFS LC-40':
        CCAFS_LC_40_df = filtered_df[filtered_df['Launch Site']=='CCAFS LC-40']
        CCAFS_LC_40 = CCAFS_LC_40_df[(CCAFS_LC_40_df['Payload Mass (kg)']>=value1[0])&(CCAFS_LC_40_df['Payload Mass (kg)']<=value1[1])]
        fig = px.scatter(CCAFS_LC_40, x="Payload Mass (kg)", y="class", color="Booster Version Category")
        return fig 

    elif entered_site == 'VAFB SLC-4E':
        VAFB_SLC_4E_df = filtered_df[filtered_df['Launch Site']=='VAFB SLC-4E']
        VAFB_SLC_4E = VAFB_SLC_4E_df[(VAFB_SLC_4E_df['Payload Mass (kg)']>=value1[0])&(VAFB_SLC_4E_df['Payload Mass (kg)']<=value1[1])]
        fig = px.scatter(VAFB_SLC_4E, x="Payload Mass (kg)", y="class", color="Booster Version Category")
        return fig 

    elif entered_site == 'KSC LC-39A':
        KSC_LC_39A_df = filtered_df[filtered_df['Launch Site']=='KSC LC-39A']
        KSC_LC_39A = KSC_LC_39A_df[(KSC_LC_39A_df['Payload Mass (kg)']>=value1[0])&(KSC_LC_39A_df['Payload Mass (kg)']<=value1[1])]
        fig = px.scatter(KSC_LC_39A, x="Payload Mass (kg)", y="class", color="Booster Version Category")
        return fig 

    else:
        CCAFS_SLC_40_df = filtered_df[filtered_df['Launch Site']=='CCAFS SLC-40']
        CCAFS_SLC_40 = CCAFS_SLC_40_df[(CCAFS_SLC_40_df['Payload Mass (kg)']>=value1[0])&(CCAFS_SLC_40_df['Payload Mass (kg)']<=value1[1])]
        fig = px.scatter(CCAFS_SLC_40, x="Payload Mass (kg)", y="class", color="Booster Version Category")
        return fig 

    
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
    