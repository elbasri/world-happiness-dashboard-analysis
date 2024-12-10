import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import os

# Define the path to the data directory
DATA_DIR = 'data/newData'

# Get a list of available years from the filenames
available_years = sorted(int(file.split('.')[0]) for file in os.listdir(DATA_DIR) if file.endswith('.csv'))

# Function to load and standardize data
def load_and_standardize_data(year):
    file_path = os.path.join(DATA_DIR, f"{year}.csv")
    data = pd.read_csv(file_path)
    
    if year in [2015, 2016]:
        data = data.rename(columns={
            'Country': 'Pays',
            'Happiness Score': 'Score',
            'Happiness Rank': 'Classement',
            'Economy (GDP per Capita)': 'PIB',
            'Health (Life Expectancy)': 'Espérance de vie',
            'Trust (Government Corruption)': 'Corruption',
            'Freedom': 'Liberté',
            'Family': 'Soutien Social',
            'Generosity': 'Générosité',
        })
    elif year == 2017:
        data = data.rename(columns={
            'Country': 'Pays',
            'Happiness.Score': 'Score',
            'Happiness.Rank': 'Classement',
            'Economy..GDP.per.Capita.': 'PIB',
            'Health..Life.Expectancy.': 'Espérance de vie',
            'Trust..Government.Corruption.': 'Corruption',
            'Family': 'Soutien Social',
            'Freedom': 'Liberté',
            'Generosity': 'Générosité',
        })
    elif year in [2018, 2019]:
        data = data.rename(columns={
            'Country or region': 'Pays',
            'Score': 'Score',
            'Overall rank': 'Classement',
            'GDP per capita': 'PIB',
            'Healthy life expectancy': 'Espérance de vie',
            'Perceptions of corruption': 'Corruption',
            'Social support': 'Soutien Social',
            'Freedom to make life choices': 'Liberté',
            'Generosity': 'Générosité',
        })
    return data

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Tableau de Bord : Bonheur Mondial"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': year, 'value': year} for year in available_years],
        value=available_years[0],
        placeholder="Sélectionnez une année"
    ),
    dcc.Graph(id='graph-score-pays'),
    dcc.Graph(id='graph-pib-score'),
    dcc.Graph(id='graph-facteurs-contribution'),
    dcc.Graph(id='graph-distribution-score'),
    dcc.Graph(id='graph-évolution-temps'),
    dcc.Graph(id='graph-freedom-score'),
    dcc.Graph(id='graph-region-distribution'),
    dcc.Graph(id='graph-top-10-happiest'),
    dcc.Graph(id='graph-heatmap-correlation'),
])

# Callback to update the charts
@app.callback(
    [
        dash.dependencies.Output('graph-score-pays', 'figure'),
        dash.dependencies.Output('graph-pib-score', 'figure'),
        dash.dependencies.Output('graph-facteurs-contribution', 'figure'),
        dash.dependencies.Output('graph-distribution-score', 'figure'),
        dash.dependencies.Output('graph-évolution-temps', 'figure'),
        dash.dependencies.Output('graph-freedom-score', 'figure'),
        dash.dependencies.Output('graph-region-distribution', 'figure'),
        dash.dependencies.Output('graph-top-10-happiest', 'figure'),
        dash.dependencies.Output('graph-heatmap-correlation', 'figure'),
    ],
    [dash.dependencies.Input('year-dropdown', 'value')]
)
def update_charts(selected_year):
    data = load_and_standardize_data(selected_year)
    
    # 1. Bar Chart: Happiness Scores by Country
    score_fig = px.bar(
        data,
        x='Pays',
        y='Score',
        title=f"Scores de Bonheur par Pays ({selected_year})",
        labels={'Score': 'Score de Bonheur'},
        hover_name='Pays'
    )
    
    # 2. Scatter Plot: GDP vs Happiness Score
    pib_fig = px.scatter(
        data,
        x='PIB',
        y='Score',
        size='Score',
        color='Soutien Social',
        title=f"Relation entre PIB et Score de Bonheur ({selected_year})",
        labels={'PIB': 'PIB par Habitants', 'Score': 'Score de Bonheur'}
    )
    
    # 3. Pie Chart: Contribution Factors
    factors = ['PIB', 'Soutien Social', 'Espérance de vie', 'Liberté', 'Générosité', 'Corruption']
    factors_data = data[factors].mean().reset_index()
    factors_data.columns = ['Facteur', 'Contribution Moyenne']
    contribution_fig = px.pie(
        factors_data,
        names='Facteur',
        values='Contribution Moyenne',
        title=f"Facteurs Contributifs au Bonheur ({selected_year})"
    )
    
    # 4. Histogram: Distribution of Scores
    distribution_fig = px.histogram(
        data,
        x='Score',
        nbins=20,
        title=f"Distribution des Scores de Bonheur ({selected_year})",
        labels={'Score': 'Score de Bonheur'}
    )
    
    # 5. Line Chart: Evolution of Scores over Time
    all_data = pd.concat([load_and_standardize_data(year) for year in available_years])
    time_fig = px.line(
        all_data,
        x='Classement',
        y='Score',
        color='Pays',
        title="Évolution des Scores de Bonheur au Fil du Temps",
        labels={'Classement': 'Classement', 'Score': 'Score de Bonheur'}
    )
    
    # 6. Scatter Plot: Freedom vs Happiness Score
    freedom_fig = px.scatter(
        data,
        x='Liberté',
        y='Score',
        size='Score',
        color='Générosité',
        title="Relation entre Liberté et Score de Bonheur",
        labels={'Liberté': 'Liberté de choix', 'Score': 'Score de Bonheur'}
    )
    
    # 7. Box Plot: Score Distribution by Region
    if 'Region' in data.columns:
        region_fig = px.box(
            data,
            x='Region',
            y='Score',
            color='Region',
            title="Distribution des Scores de Bonheur par Région",
            labels={'Score': 'Score de Bonheur', 'Region': 'Région'}
        )
    else:
        region_fig = {}

    # 8. Bar Chart: Top 10 Happiest Countries
    top_10_happiest = data.nlargest(10, 'Score')
    happiest_fig = px.bar(
        top_10_happiest,
        x='Pays',
        y='Score',
        title="Top 10 des Pays les Plus Heureux",
        labels={'Pays': 'Pays', 'Score': 'Score de Bonheur'},
        color='Score'
    )
    
    # 9. Heatmap: Correlation between Factors
    correlation_matrix = data[factors + ['Score']].corr()
    heatmap_fig = px.imshow(
        correlation_matrix,
        text_auto=True,
        title="Carte de Corrélation des Facteurs",
        labels=dict(color="Corrélation")
    )
    
    return score_fig, pib_fig, contribution_fig, distribution_fig, time_fig, freedom_fig, region_fig, happiest_fig, heatmap_fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
