import dash
from dash import dcc, html, Dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

load_figure_template('CYBORG')

# Load the data
data = pd.read_excel(r'C:\Users\Dell\OneDrive\Desktop\advance web scraping\Nakri_data_set\Skill_Gap_Analysis_Tool\notebooks\result.xlsx')

# Drop unnecessary columns
data = data.drop(columns=['is_remote'])

# Filter top 20 companies
company_pay = data.groupby('Company')['job_pay'].sum().reset_index()
top_companies = company_pay.nlargest(20, 'job_pay')['Company']
filtered_data = data[data['Company'].isin(top_companies)]

# Calculate statistics
total_job = data.shape[0]
companies = data['Company'].nunique()
location = data['location'].nunique()
min_value = data['job_pay'].min()
max_value = data['job_pay'].max()

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Create plots
count_plot = px.bar(data, x='Job_role', 
                    category_orders={'Job_role': data['Job_role'].value_counts().index},
                    title='Distribution of Job Roles')
count_plot.update_layout(xaxis_title='Job Role', yaxis_title='Count', xaxis_tickangle=-45)

histogram = px.histogram(data, x='job_pay', nbins=20, title='Distribution of Job Pay')
histogram.update_layout(xaxis_title='Job Pay', yaxis_title='Frequency')

sunburst_chart = px.sunburst(filtered_data, 
                             path=['Company Size', 'Company', 'Job Category', 'Primary Skill Category', 'Job_role'], 
                             values='job_pay', 
                             title='Sunburst Chart: Top 20 Companies by Job Pay')

treemap_company_size = px.treemap(data, path=['Company Size', 'Company'], values='job_pay', title='Distribution of Companies by Size')
treemap_job_roles_location = px.treemap(data, path=['location', 'Job_role'], values='job_pay', title='Distribution of Job Roles by Location')
treemap_skill_category = px.treemap(data, path=['Primary Skill Category', 'Job_role'], values='job_pay', title='Job Roles by Primary Skill Category')

# Function to get top N categories
def get_top_categories(column, n=5):
    top_categories = data[column].value_counts().nlargest(n).index.tolist()
    return data[data[column].isin(top_categories)]

top_job_roles = get_top_categories('Job_role')
top_skill_categories = get_top_categories('Primary Skill Category')
top_company_sizes = get_top_categories('Company Size')

app = Dash(title='Skill Analysis', external_stylesheets=[dbc.themes.CYBORG])

server = app.server

# Layout
app.layout = dbc.Container([
    html.Div([
        html.H1('Job Skill DATA ANALYSIS', style={
            'textAlign': 'center',
            'color': 'white',
            'fontSize': '28px',
            'marginTop': '35px',
            'marginBottom': '5px',
            'fontFamily': 'Roboto, sans-serif',
            'fontWeight': 'bold',
            'padding': '10px'
        }),
        html.H1('Explore relation between jobs that are most required and additional information of the job roles', style={
            'fontSize': '15px',
            'textAlign': 'center',
            'fontWeight': 'bold',
        }),
    ]),
    ###################------------------------5 statistic card-----------------------------------
    dbc.Row([
        dbc.Col(html.Div([
            html.H6("Total Job", style={'color': 'black'}),
            html.H5(f"{total_job}", style={'color': 'black'})
        ], style={
            'textAlign': 'center',
            'color': 'red',
            'fontWeight': 'bold 4px',
            'borderRadius': '10%',
            'backgroundColor': 'white'
        }), width=2),
        dbc.Col(html.Div([
            html.H6("Total unique companies", style={'color': 'black'}),
            html.H5(f"{companies}", style={'color': 'black'})
        ], style={
            'textAlign': 'center',
            'color': 'red',
            'fontWeight': 'bold 4px',
            'borderRadius': '10%',
            'backgroundColor': 'white'
        }), width=2),
        dbc.Col(html.Div([
            html.H6("Different locations", style={'color': 'black'}),
            html.H5(f"{location}", style={'color': 'black'})
        ], style={
            'textAlign': 'center',
            'color': 'red',
            'fontWeight': 'bold 4px',
            'borderRadius': '10%',
            'backgroundColor': 'white'
        }), width=2),
        dbc.Col(html.Div([
            html.H6("Min pay", style={'color': 'black'}),
            html.H5(f"{min_value:.2f}", style={'color': 'black'})
        ], style={
            'textAlign': 'center',
            'color': 'red',
            'fontWeight': 'bold 4px',
            'borderRadius': '10%',
            'backgroundColor': 'white'
        }), width=2),
        dbc.Col(html.Div([
            html.H6("Max Pay", style={'color': 'black'}),
            html.H5(f"{max_value:.2f}", style={'color': 'black'})
        ], style={
            'textAlign': 'center',
            'fontWeight': '2398923',
            'borderRadius': '10%',
            'backgroundColor': 'white'
        }), width=2)
    ], className='statistics'),
    #############-----------------------3 pie graph---------------------------------##########################
    dbc.Row([
        dbc.Col(dcc.Graph(
            figure=px.pie(top_job_roles, names='Job_role', title='Top Job Roles'),
            style={'height': '300px', 'marginTop': '15px','marginBottom': '15px', 'width': '100%'}
        ), width=4),
        dbc.Col(dcc.Graph(
            figure=px.pie(top_skill_categories, names='Primary Skill Category', title='Top Skill Categories'),
            style={'height': '300px',  'marginTop': '15px','marginBottom': '15px','width': '100%'}
        ), width=4),
        dbc.Col(dcc.Graph(
            figure=px.pie(top_company_sizes, names='Company Size', title='Top Company Sizes'),
            style={'height': '300px', 'width': '100%', 'marginTop': '15px','marginBottom': '15px',}
        ), width=4)
    ]),
    ################----------------------3 drop down for the stackbar------------------------------
    dbc.Row([
        dbc.Col([
            html.H6("Select Any Col"),
            dcc.Dropdown(
                
                id='x-axis-dropdown',
                options=[{'label': col, 'value': col} for col in data.columns],
                value='job_pay',
                clearable=False
            ),
        ], width=2),
        dbc.Col([
            html.H6("Select Any Col"),
            dcc.Dropdown(
                
                id='y-axis-dropdown',
                options=[{'label': col, 'value': col} for col in data.columns],
                value='review',
                clearable=False,
                
            ),
            
        ], width=2),
        dbc.Col([
            html.H6("Select Company Size"),
            dcc.Dropdown(
                id='company-size-dropdown',
                options=[{'label': size, 'value': size} for size in data['Company Size'].unique()],
                clearable=False,
                
            ),
        ], width=2),
        
    ]),
    ################ --------------------------- Check list for  stackbar---------------------------
    dbc.Row([
        dbc.Col([
            html.H6("Select Branches"),
            dcc.Checklist(
                id='branches-checklist',
                options=[
                    {'label': 'Has more than 3 branches', 'value': 1},
                    {'label': 'Has 3 or fewer branches', 'value': 0}
                ],
                value=[1, 0],
                inline=True
            ),
        ], width=2),

        

    ]),

    ##############--------------------------------- slider for stack bar ---------------------------
    dbc.Row([
        dbc.Col([
             html.H6("Select Top 40 Company"),  # Add your heading here

            dcc.Slider(
                id='top-n-slider',
                min=1,
                max=40,
                step=1,
                value=20,
                marks={i: str(i) for i in range(1, 41)}
                
            ),
        ] ,style={'margin-top': '45px'}, width=8)

    ]),

    ################### ------------- drop down for Bar gragh ---------------------
    
     dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col(width=9),  # Empty column to push content to the right
                dbc.Col([
                    html.H6("Select Job Role"),  # Add your heading here
                    dcc.Dropdown(
                        id='role-dropdown',
                        options=[{'label': role, 'value': role} for role in data['Job_role']],
                        value=data['Job_role'][0],
                        clearable=False
                    ),
                ], width=3),
            ]),
            dbc.Row([
                dbc.Col(width=7),  # Empty column to push content to the right
                dbc.Col([
                    html.H6("Select Experience"),
                    dcc.Slider(
                        id='year-slider',
                        min=min(data['max_year']),
                        max=max(data['max_year']),
                        step=1,
                        value=sum(data['max_year']) / len(data['max_year']),
                        marks={i: str(i) for i in range(min(data['max_year']), max(data['max_year']) + 1)},
                    ),
                ], width=5),
            ]),
        ], width=12)
    ]),
    ################ --------------------- both the graph -----------------------------------
    dbc.Row([
        
        dbc.Col([
            dcc.Graph(id='stacked-bar-chart')
        ], width=6),
        dbc.Col([
            dcc.Graph(id='bar-chart')
        ], width=6)
    ]),
    ###############----------------- 2 gragh in a row histogram , count_plot----------------------
    dbc.Row([
        dbc.Col(dcc.Graph(
            figure=count_plot,
            style={'height': '400px'}
        ), width=6),
        dbc.Col(dcc.Graph(
            figure=histogram,
            style={'height': '400px'}
        ), width=6)
    ]),
    ##########----------------------------sunburtst -----------------------------------
    dbc.Row([
        dbc.Col(dcc.Graph(
            figure=sunburst_chart,
            style={'height': '600px'}
        ), width=12)
    ]),
    #############-------------------------- tree grapgh-----------------------------------
    dbc.Row([
        dbc.Col(dcc.Graph(
            figure=treemap_company_size,
            style={'height': '400px'}
        ), width=4),
        dbc.Col(dcc.Graph(
            figure=treemap_job_roles_location,
            style={'height': '400px'}
        ), width=4),
        dbc.Col(dcc.Graph(
            figure=treemap_skill_category,
            style={'height': '400px'}
        ), width=4)
    ]),
    
    html.Label("Select Job Role:"),
    dcc.Dropdown(
        id='job-role-dropdown',
        options=[{'label': role, 'value': role} for role in data['Job_role'].unique()],
        value=data['Job_role'].unique()[0],
        style={'width': '50%'}
    ),
    
    html.Label("Filter by Years of Experience:"),
    dcc.Slider(
        id='experience-slider',
        min=data['max_year'].min(),
        max=data['max_year'].max(),
        step=1,
        marks={i: f'{i}' for i in range(data['max_year'].min(), data['max_year'].max() + 1)},
        value=data['max_year'].max(),
    ),
    
    dcc.Graph(id='bar-plot')
],fluid=True)

# Callback to update the bar plot based on the dropdown and slider values
@app.callback(
    Output('bar-plot', 'figure'),
    [Input('job-role-dropdown', 'value'),
     Input('experience-slider', 'value')]
)
def update_bar_plot(selected_role, selected_year):
    if selected_role not in data['Job_role'].unique():
        fig = px.bar(title="Invalid job role selected")
        return fig

    filtered_data1 = data[(data['Job_role'] == selected_role) & (data['max_year'] <= selected_year)]
    
    if filtered_data1.empty:
        fig = px.bar(title=f"No jobs found for {selected_role} with up to {selected_year} years of experience")
    else:
        top_data = filtered_data1.sort_values(by='job_pay', ascending=False).head(10)
        fig = px.bar(top_data, x='Company', y='job_pay', color='Company', title=f'Top 10 {selected_role} Jobs with Max {selected_year} Years of Experience')
    
    return fig

# Callbacks to update the graphs
@app.callback(
    [Output('stacked-bar-chart', 'figure'),
     Output('bar-chart', 'figure')],
    [Input('x-axis-dropdown', 'value'),
     Input('y-axis-dropdown', 'value'),
     Input('company-size-dropdown', 'value'),
     Input('branches-checklist', 'value'),
     Input('top-n-slider', 'value'),
     Input('role-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_graphs(x_axis, y_axis, company_size, branches_status, top_n, selected_role, selected_year):
    filtered_data = data[(data['Company Size'] == company_size) &
                         (data['+3_branches'].isin(branches_status))]
    
    top_filtered_data = filtered_data.sort_values(by=x_axis, ascending=False).head(top_n)
    
    stacked_bar_fig = px.bar(top_filtered_data, x=x_axis, y=y_axis, color='Company Size', 
                             title=f'Top {top_n} by {x_axis} and {y_axis}', orientation='h')
    
    bar_fig = update_bar_plot(selected_role, selected_year)
    
    return stacked_bar_fig, bar_fig

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)

