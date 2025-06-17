# app.py
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# --- 1. Load and Prepare Data ---
# Load the dataset
df = pd.read_csv("internship_data.csv")
# Convert 'application_date' to datetime objects for proper sorting and filtering
df['application_date'] = pd.to_datetime(df['application_date'])
# Extract the year for trend analysis
df['year'] = df['application_date'].dt.year

# --- 2. Perform Analysis ---
# Analysis 1: Most Popular Domains (Overall)
domain_popularity = df['domain'].value_counts().reset_index()
domain_popularity.columns = ['Domain', 'Number of Applications']

# Analysis 2: Application Trends Over Time
yearly_trends = df.groupby(['year', 'domain']).size().reset_index(name='count')

# --- 3. Create Visualizations with Plotly Express ---
# Figure 1: Bar chart for most popular domains
fig_popularity = px.bar(
    domain_popularity,
    x='Number of Applications',
    y='Domain',
    orientation='h',
    title='Most Popular Internship Domains (Overall)',
    labels={'Domain': '', 'Number of Applications': 'Total Applications'},
    template='plotly_white',
    color='Number of Applications',
    color_continuous_scale=px.colors.sequential.Indigo
).update_yaxes(categoryorder='total ascending').update_layout(showlegend=False)

# Figure 2: Line chart for emerging trends
fig_trends = px.line(
    yearly_trends,
    x='year',
    y='count',
    color='domain',
    title='Emerging Internship Domain Trends (2021-2024)',
    labels={'year': 'Year', 'count': 'Number of Applications', 'domain': 'Domain'},
    markers=True,
    template='plotly_white'
)
# Make x-axis ticks integers (e.g., 2021, 2022)
fig_trends.update_xaxes(dtick=1)

# --- 4. Initialize the Dash App ---
app = dash.Dash(__name__)
server = app.server # Expose server for deployment platforms

# --- 5. Define the App Layout ---
app.layout = html.Div(style={'backgroundColor': '#f8f9fa', 'fontFamily': 'Arial, sans-serif', 'padding': '2rem'}, children=[
    
    # Header
    html.Div(style={'textAlign': 'center', 'marginBottom': '40px'}, children=[
        html.H1("MITS Internship Engagement Dashboard", style={'color': '#2c3e50', 'fontWeight': 'bold'}),
        html.P("Analysis of student application and participation data.", style={'color': '#7f8c8d', 'fontSize': '1.2rem'})
    ]),
    
    # Main Content Area - Visualizations
    html.Div(className='main-content', style={'backgroundColor': '#ffffff', 'padding': '30px', 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}, children=[
        
        # Section 1: Overall Popularity
        html.H2("Overall Domain Popularity", style={'borderBottom': '2px solid #e0e0e0', 'paddingBottom': '10px'}),
        html.P("This chart shows the total number of applications received for each domain since 2021. It helps identify the all-time most sought-after fields.", style={'color': '#555'}),
        dcc.Graph(
            id='popularity-chart',
            figure=fig_popularity
        ),
        
        html.Hr(style={'margin': '40px 0'}),
        
        # Section 2: Trends Over Time
        html.H2("Emerging and Declining Trends", style={'borderBottom': '2px solid #e0e0e0', 'paddingBottom': '10px'}),
        html.P("The line chart tracks application numbers year-over-year. Watch for lines with a steep upward slope—these are the 'emerging' domains.", style={'color': '#555'}),
        dcc.Graph(
            id='trends-chart',
            figure=fig_trends
        )
    ]),
    
    # Footer
    html.Footer(style={'textAlign': 'center', 'marginTop': '40px', 'padding': '20px', 'color': '#95a5a6'}, children=[
        html.P("© 2024 Micro Information Technology Services (MITS) | Data Analytics Division")
    ])
])

# --- 6. Run the App ---
if __name__ == '__main__':
    app.run_server(debug=True)
