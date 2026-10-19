
# 🏡 King County Real Estate Valuation & Analytics Dashboard

An end-to-end Machine Learning and interactive dashboard project built with **Plotly Dash**, **Bootstrap**, and **XGBoost** to predict house prices and analyze geospatial housing trends across King County, Washington (including Seattle, Bellevue, Redmond, Kirkland, and surrounding areas). Developed as a capstone project for the **Digital Egypt Pioneers Initiative (DEPI)**.

---

## 👥 Project Team

* **Mohamed Elmhlawy**
* **Zeyad Elshiekh**
* **Mohned Hamed**
* **Omar Marzouk**
* **Mahmoud Samir**
* **Menna Sokar**

---

## 📁 Project Structure


```

├── app.py                      # Main Dash web application (clean, simple entrypoint)
├── data_loader.py              # Data loading, prediction engine & Plotly chart builders
├── requirements.txt            # Python dependencies
├── .gitignore                  # Standard Python & Jupyter ignore rules
├── README.md                   # Project documentation
│
├── assets/                     # Dashboard styles
│   └── custom.css              # Custom CSS styling (Inter font, cards, badges)
│
├── layouts/                    # Modular layout components
│   ├── **init**.py             # Layout package exports
│   ├── header.py               # Navigation banner & KPI summary metrics
│   ├── prediction_tab.py       # Tab 1: Feature inputs & interactive map
│   ├── visualizations_tab.py   # Tab 2: EDA charts from Visualization.ipynb
│   ├── ml_tab.py               # Tab 3: Model comparison & "Why XGBoost"
│   ├── dataset_tab.py          # Tab 4: Sample data table & data dictionary
│   └── footer.py               # Footer component
│
├── Notebooks/                  # Research & exploration notebooks
│   ├── Cleaning.ipynb          # Data cleaning, null handling & feature engineering
│   ├── MachineLearning.ipynb   # Model training & benchmarking (XGBoost, RF, Ridge, OLS)
│   └── Visualization.ipynb     # In-depth exploratory data analysis visualizations
│
└── Data/                       # Datasets & serialized models
├── CleanedData.csv         # Final processed dataset (21,612 records)
├── kc_house_data_NaN.csv   # Raw King County housing data
├── best_house_price_model.pkl # Trained champion XGBoost model
└── model_features.pkl      # Feature columns list for model inference

```

---

## 🌟 Dashboard Features & Sections

### 1. 🔮 House Price Prediction & Interactive Map (Main Section)
- **Live Machine Learning Valuation:** Predicts house price in real-time (< 5ms inference latency) based on 21 structural, quality, and location features.
- **Interactive Inputs:**
  - **Living Space:** Bedrooms, Bathrooms, Interior Area (sq ft), Lot Area (sq ft), Floors, Basement.
  - **Quality & Condition:** Construction Grade (1–13), Condition (1–5), View Quality (0–4), Waterfront status.
  - **Location & Coordinates:** Zipcode dropdown (auto-fills centroid latitude & longitude), direct coordinate inputs.
  - **Age & Renovation:** Year Built, Renovation status, Year Renovated, Neighborhood living and lot areas (15 nearest neighbors).
- **Interactive King County Map:**
  - Displays comparable sales (comps) with real OpenStreetMap tiles, colored by price gradient.
  - **Highlighted Target Property:** Places a **glowing crimson pin marker** with a valuation badge directly at the targeted house's coordinates.
  - **Click-to-Locate:** Clicking anywhere on the map dynamically updates Latitude, Longitude, and nearest Zipcode in the form, automatically re-running the valuation!
- **One-Click Test Presets:**
  - 🏡 *Seattle Standard Home* (3 bed, 2 bath, 1,800 sq ft, Grade 7, Zip 98103)
  - 💎 *Bellevue Luxury Mansion* (5 bed, 4.5 bath, 4,800 sq ft, Grade 11, Zip 98004)
  - 🌊 *Mercer Island Waterfront Estate* (4 bed, 4 bath, 4,200 sq ft, Grade 12, Waterfront, Zip 98004)
  - 🌲 *Suburban Family Home* (3 bed, 1.75 bath, 1,500 sq ft, Grade 7, Zip 98001)

---

### 2. 📊 Exploratory Visualizations Section
Replicates all 9 interactive visualizations from `Notebooks/Visualization.ipynb`:
1. **Real Geographic Housing Map:** 5,000 sampled transactions on OpenStreetMap with living area bubble sizing and price colormaps.
2. **Price Skewness & Log-Transformation:** Raw price skewness (+4.02) normalized to +0.43 via `np.log1p`.
3. **Living Area vs Price & Log Price:** Dual scatter with OLS regression fit lines showing variance stabilization.
4. **Lot Space & Density Analysis:** Living area vs lot area on log-scale and living-to-lot ratio vs log price.
5. **Correlation Matrix Heatmap:** Top 12 numerical predictors of property price.
6. **Construction Grade & Waterfront Impact:** Log-scale boxplot demonstrating the substantial premium of waterfront locations across all construction grades.
7. **Geospatial Density & Mean Price:** Spatial sales volume density versus geographic average price clusters around Lake Washington.
8. **3D Surface & Scatter Explorer:** Interactive 3D visualization of Living Area vs Grade vs Log Price colored by Price per Sq Ft.
9. **House Prices by Postal Zipcode:** Top 15 most expensive zipcodes (Medina $1.89M, Bellevue $1.15M) vs top 15 most affordable zipcodes ($235k - $278k).

---

### 3. 🤖 Machine Learning & "Why We Used XGBoost" Section
- **Benchmark Comparison Table & Graphs:**
  - **XGBoost Regressor:** $R^2 = \mathbf{90.98\%}$, $\text{MAE} = \mathbf{\$64,599}$, $\text{RMSE} = \mathbf{\$119,933}$ 🏆 *(Selected Champion)*
  - **Random Forest:** $R^2 = 88.98\%$, $\text{MAE} = \$72,425$, $\text{RMSE} = \$139,933$
  - **Polynomial Ridge Regression:** $R^2 = 83.21\%$, $\text{MAE} = \$92,827$, $\text{RMSE} = \$164,025$
  - **Linear Regression:** $R^2 = 77.81\%$, $\text{MAE} = \$113,987$, $\text{RMSE} = \$255,705$
- **Evaluation Visualizations:**
  - $R^2$ Score Comparison Bar Chart (Higher is better)
  - Mean Absolute Error ($) Comparison Bar Chart (Lower is better)
  - Actual vs Predicted Price Scatter Plot on log-log scale with $y=x$ ideal identity line
  - Residual Error Distribution centered at $\$0$
  - Feature Importance Ranking Bar Chart (Construction Grade 48.1%, Latitude 14.2%, Living Area 11.9%, Waterfront 4.5%, etc.)
- **Why We Chose XGBoost (Key Reasons):**
  1. *Non-Linear Interaction Modeling:* Captures multi-way interactions (e.g. Waterfront × Grade × Square Footage) without manual polynomial expansion.
  2. *Empirical Superiority:* Slashed MAE by >$49,300 compared to linear regression and beat Random Forest by >$7,800 per house.
  3. *Built-in L1/L2 Regularization:* Penalizes complex trees, preventing overfitting on 21,600+ records.
  4. *Gradient Boosting Mechanism:* Sequentially targets hard-to-value luxury and edge-case homes.
  5. *Geospatial Partitioning:* Recursive tree splits naturally isolate high-value micro-neighborhoods.
  6. *Ultra-low Latency:* Sub-5ms inference speed allows instantaneous interactive dashboard updates.

---

### 4. 📁 Dataset Explorer & Data Dictionary
- Interactive sample table of the 21,612 cleaned property transactions.
- Complete data dictionary describing all 21 raw and engineered features.

---

## 🚀 Getting Started (Run Locally)

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/king-county-real-estate-valuation.git](https://github.com/your-username/king-county-real-estate-valuation.git)
   cd king-county-real-estate-valuation

```

2. **Install dependencies:**
```bash
pip install -r requirements.txt

```


3. **Run the dashboard:**
```bash
python app.py

```


4. **Open in your browser:**
```
[http://127.0.0.1:8050/](http://127.0.0.1:8050/)

```



---

## 📓 Running the Notebooks

The Jupyter Notebooks are located in the `Notebooks/` directory and are configured to read data directly from `../Data/`:

* `Notebooks/Cleaning.ipynb`: Data cleaning, imputing, and feature engineering.
* `Notebooks/Visualization.ipynb`: Exploratory data analysis charts.
* `Notebooks/MachineLearning.ipynb`: Model training, evaluation, and serialization.

---

## 🎓 Acknowledgments

This project was developed under the **Digital Egypt Pioneers Initiative (DEPI)** - Data Science Track. Special thanks to our instructors and mentors for their guidance throughout the program.

```

<FollowUp label="Would you like a footer component or 'About the Team' modal script for your Plotly Dash web app?" query="Show me how to add a clean 'About the Team & DEPI Project' section or modal inside the Plotly Dash app interface."/>

```
