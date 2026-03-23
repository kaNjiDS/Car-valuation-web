# Car Valuation Web Application

This project demonstrates an interactive **Data-Driven Vehicle Price
Prediction System** built using **Streamlit** and **Machine Learning**.

------------------------------------------------------------------------

## Technologies Used

-   Python 3
-   Streamlit
-   Pandas
-   NumPy
-   Scikit-learn
-   Plotly (for interactive visualizations)

## How It Works

1.  User opens the web application.
2.  User explores dataset through interactive dashboards.
3.  User inputs vehicle details (brand, fuel type, engine size, etc) and filter the dataset.
4.  User can explore the key factors that affected to the vehicle price.
5.  The trained Gradient Boosting model processes the inputs.
6.  The system predicts the vehicle price.
7.  Results are displayed with price estimate, range, and insights.

## Features

-   Data Explorer
-   Interactive Visualisations
-   Price Predictor
-   Statistical Analysis
-   Modern UI

## Running the Project

``` bash
git clone <https://github.com/kaNjiDS/Car-valuation-web.git>
cd Car-valuation-web
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run Home.py
```

## Access

http://localhost:8501

## Model Performance

-   R²: 0.928
-   MAPE: 12.2%

## Author
s16829 \| ST3011 \| Group 7
