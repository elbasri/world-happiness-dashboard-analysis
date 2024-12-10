
# World Happiness Dashboard Analysis

An interactive web application built with **Dash** and **Plotly** that visualizes data from the World Happiness Report across multiple years. This dashboard allows users to explore trends, correlations, and key factors contributing to happiness worldwide.

---

## Features

1. **Interactive Visualizations:**
   - Bar chart: Happiness scores by country.
   - Scatter plot: GDP vs. Happiness score.
   - Pie chart: Contribution of factors like GDP, social support, and life expectancy.
   - Histogram: Distribution of happiness scores.
   - Line chart: Evolution of happiness scores over time.
   - Scatter plot: Freedom vs. Happiness score.
   - Box plot: Happiness score distribution by region.
   - Bar chart: Top 10 happiest countries.
   - Heatmap: Correlation between happiness factors.

2. **Dynamic Year Selection:**
   - Easily switch between datasets for years 2015–2019 using a dropdown menu.

3. **Localization:**
   - All titles and labels are in French.

---

## Getting Started

### Prerequisites

Ensure you have Python 3.7 or later installed on your machine. Install the required Python libraries using:

```bash
pip install dash pandas plotly
```

### Clone the Repository

```bash
git clone https://github.com/elbasri/world-happiness-dashboard-analysis.git
cd world-happiness-dashboard-analysis
```

### Data Preparation

1. Place the World Happiness Report CSV files for years 2015–2019 in a folder named `data/newData` relative to the app script.
2. Ensure the files follow the naming convention: `2015.csv`, `2016.csv`, ..., `2019.csv`.

### Running the App

Run the app locally:

```bash
python app.py
```

Open your browser and navigate to [http://127.0.0.1:8050](http://127.0.0.1:8050).

---

## File Structure

```
world-happiness-dashboard-analysis/
│
├── app.py                # Main Dash application
├── README.md             # Documentation
├── data/
│   └── newData/          # Directory containing CSV files (2015.csv, 2016.csv, etc.)
└── requirements.txt      # Python dependencies
```


## Deployment

### Local Deployment

Follow the steps in [Getting Started](#getting-started) to run the app locally.

### Cloud Deployment

You can deploy the app to cloud platforms like **Heroku** or **Render**:

1. Add a `requirements.txt`:
   ```bash
   pip freeze > requirements.txt
   ```

2. Add a `Procfile` for Heroku:
   ```bash
   echo "web: python app.py" > Procfile
   ```

3. Push to your Heroku app repository:
   ```bash
   git add .
   git commit -m "Deploy World Happiness Dashboard Analysis"
   git push heroku master
   ```

---

## License

This project is licensed under the MIT License.

---

## Acknowledgements

- [World Happiness Report](https://www.kaggle.com/datasets/unsdsn/world-happiness) for the dataset.
- [Dash](https://dash.plotly.com/) for building interactive web apps.
- [Plotly](https://plotly.com/) for powerful visualizations.

## Author

Developed by **ABDENNACER Elbasri** | Twitter: **@abdennacerelb** | Linkedin **@elbasri**.