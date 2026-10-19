"""
data_loader.py
Backend data loading, caching, model prediction, and visualization generators
for the King County House Price Prediction & Analytics Dash Dashboard.
"""

import os
import pickle
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.model_selection import train_test_split

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'Data', 'CleanedData.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'Data', 'best_house_price_model.pkl')
FEATURES_PATH = os.path.join(BASE_DIR, 'Data', 'model_features.pkl')

# -------------------------------------------------------------
# 1. LOAD DATASET & MODEL
# -------------------------------------------------------------
print("Loading dataset from:", DATA_PATH)
df = pd.read_csv(DATA_PATH)
if 'Unnamed: 0' in df.columns:
    df = df.drop(columns=['Unnamed: 0'])

print("Loading trained model and features...")
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

with open(FEATURES_PATH, 'rb') as f:
    feature_cols = pickle.load(f)

# Zipcode centroids for map and auto-fill
zip_coords = df.groupby('zipcode')[['lat', 'long']].mean().round(5).to_dict(orient='index')
zipcode_list = sorted(list(zip_coords.keys()))
zip_centers_df = df.groupby('zipcode')[['lat', 'long']].mean().reset_index()

def find_nearest_zipcode(lat: float, lon: float) -> int:
    """Finds the closest King County zipcode centroid given lat & lon."""
    dists = (zip_centers_df['lat'] - lat)**2 + (zip_centers_df['long'] - lon)**2
    return int(zip_centers_df.loc[dists.idxmin(), 'zipcode'])

# -------------------------------------------------------------
# 2. MODEL METRICS & PRE-COMPUTED TEST EVALUATION
# -------------------------------------------------------------
# Exact evaluation numbers from MachineLearning.ipynb
MODEL_COMPARISON = pd.DataFrame([
    {
        'Model': 'XGBoost',
        'R2 Score': 0.909803,
        'RMSE ($)': 119932.59,
        'MAE ($)': 64599.45,
        'Training Time': 'Fast (Parallel)',
        'Status': '🏆 Selected Best Model'
    },
    {
        'Model': 'Random Forest',
        'R2 Score': 0.889783,
        'RMSE ($)': 139933.32,
        'MAE ($)': 72425.40,
        'Training Time': 'Moderate',
        'Status': 'Benchmark 2nd'
    },
    {
        'Model': 'Polynomial Regression',
        'R2 Score': 0.832066,
        'RMSE ($)': 164024.75,
        'MAE ($)': 92827.07,
        'Training Time': 'Moderate (Ridge)',
        'Status': 'Overfitting Risk'
    },
    {
        'Model': 'Linear Regression',
        'R2 Score': 0.778078,
        'RMSE ($)': 255705.38,
        'MAE ($)': 113986.74,
        'Training Time': 'Instant',
        'Status': 'Baseline'
    }
])

# Feature Importances
feature_importances = pd.Series(
    model.feature_importances_, 
    index=feature_cols
).sort_values(ascending=False).reset_index()
feature_importances.columns = ['Feature', 'Importance']

# Friendly names for feature importance
FEATURE_LABELS = {
    'grade': 'Construction Grade (1-13)',
    'lat': 'Latitude (Location/North-South)',
    'sqft_living': 'Interior Living Area (sq ft)',
    'waterfront': 'Waterfront Property (Flag)',
    'view': 'Scenic View Quality (0-4)',
    'house_age': 'Age of Property (Years)',
    'sqft_living15': 'Living Area of 15 Neighbors',
    'long': 'Longitude (Location/East-West)',
    'zipcode': 'Postal Zipcode Area',
    'condition': 'Property Condition (1-5)',
    'sale_year': 'Year of Sale',
    'bathrooms': 'Number of Bathrooms',
    'sqft_lot15': 'Lot Area of 15 Neighbors',
    'sqft_lot': 'Lot Area (sq ft)',
    'living_to_lot_ratio': 'Living-to-Lot Area Ratio',
    'years_since_renovation': 'Years Since Last Renovation',
    'floors': 'Number of Floors',
    'is_renovated': 'Renovation Status (Flag)',
    'has_basement': 'Basement Present (Flag)',
    'sale_month': 'Month of Sale',
    'bedrooms': 'Number of Bedrooms'
}
feature_importances['Feature_Label'] = feature_importances['Feature'].map(FEATURE_LABELS).fillna(feature_importances['Feature'])

# Compute test predictions for evaluation plots (sample 2,000 for responsive graph)
X = df[feature_cols]
y = df['log_price']
_, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
test_preds_log = model.predict(X_test)
test_actual = np.expm1(y_test)
test_predicted = np.expm1(test_preds_log)
test_df = pd.DataFrame({
    'Actual_Price': test_actual,
    'Predicted_Price': test_predicted,
    'Residual': test_actual - test_predicted,
    'Abs_Error': np.abs(test_actual - test_predicted)
})

# Subsample dataset for fast responsive UI visualizations
df_sample_map = df.sample(n=min(5000, len(df)), random_state=42).copy()
df_sample_viz = df.sample(n=min(3500, len(df)), random_state=42).copy()
p1, p99 = df['price'].quantile(0.01), df['price'].quantile(0.99)

# -------------------------------------------------------------
# 3. PREDICTION ENGINE
# -------------------------------------------------------------
def predict_house_price(
    bedrooms: float,
    bathrooms: float,
    sqft_living: float,
    sqft_lot: float,
    floors: float,
    waterfront: int,
    view: int,
    condition: int,
    grade: int,
    zipcode: int,
    lat: float,
    long: float,
    sqft_living15: float,
    sqft_lot15: float,
    has_basement: int,
    yr_built: int,
    is_renovated: int,
    yr_renovated: int,
    sale_year: int = 2015,
    sale_month: int = 6
):
    """
    Computes engineered features and evaluates the trained XGBoost model.
    Returns:
        dict containing predicted price, confidence range, price per sqft, and stats.
    """
    house_age = max(0, sale_year - yr_built)
    if is_renovated == 1 and yr_renovated > 0:
        years_since_renovation = max(0, sale_year - yr_renovated)
    else:
        years_since_renovation = house_age

    living_to_lot_ratio = sqft_living / max(1.0, sqft_lot)

    input_data = pd.DataFrame([{
        'bedrooms': float(bedrooms),
        'bathrooms': float(bathrooms),
        'sqft_living': float(sqft_living),
        'sqft_lot': float(sqft_lot),
        'floors': float(floors),
        'waterfront': int(waterfront),
        'view': int(view),
        'condition': int(condition),
        'grade': int(grade),
        'zipcode': int(zipcode),
        'lat': float(lat),
        'long': float(long),
        'sqft_living15': float(sqft_living15),
        'sqft_lot15': float(sqft_lot15),
        'has_basement': int(has_basement),
        'sale_year': int(sale_year),
        'sale_month': int(sale_month),
        'house_age': float(house_age),
        'is_renovated': int(is_renovated),
        'years_since_renovation': float(years_since_renovation),
        'living_to_lot_ratio': float(living_to_lot_ratio)
    }])[feature_cols]

    log_pred = model.predict(input_data)[0]
    pred_price = float(np.expm1(log_pred))

    # Calculate confidence interval based on test MAE (~$64.6k or ~11%)
    mae_val = 64599.45
    min_range = max(50000.0, pred_price - mae_val)
    max_range = pred_price + mae_val

    price_per_sqft = pred_price / max(1.0, sqft_living)

    # Classify valuation tier
    if pred_price < 350000:
        tier = "Affordable Starter / Suburban"
        tier_color = "success"
    elif pred_price < 650000:
        tier = "Mid-Market Residential"
        tier_color = "primary"
    elif pred_price < 1200000:
        tier = "Premium / Upper-Tier Executive"
        tier_color = "warning"
    else:
        tier = "Luxury & Waterfront Estate"
        tier_color = "danger"

    return {
        'predicted_price': pred_price,
        'min_range': min_range,
        'max_range': max_range,
        'price_per_sqft': price_per_sqft,
        'tier': tier,
        'tier_color': tier_color,
        'house_age': house_age,
        'years_since_renovation': years_since_renovation,
        'living_to_lot_ratio': living_to_lot_ratio
    }

# -------------------------------------------------------------
# 4. MAIN MAP GENERATOR
# -------------------------------------------------------------
def build_main_map(
    target_lat: float = 47.67,
    target_lon: float = -122.34,
    target_price: float = None,
    target_label: str = "Selected Target Property",
    max_price_filter: float = 2500000.0,
    waterfront_only: bool = False
):
    """
    Builds the interactive King County map displaying comparable sales
    and highlighting the user's targeted property with a high-visibility marker.
    """
    map_data = df_sample_map.copy()
    if waterfront_only:
        map_data = map_data[map_data['waterfront'] == 1]
    if max_price_filter:
        map_data = map_data[map_data['price'] <= max_price_filter]

    fig = px.scatter_map(
        map_data,
        lat='lat',
        lon='long',
        color='price',
        size='sqft_living',
        size_max=12,
        color_continuous_scale='Viridis',
        range_color=[p1, min(p99, max_price_filter)],
        zoom=9.2,
        center=dict(lat=target_lat if target_lat else 47.56, lon=target_lon if target_lon else -122.25),
        map_style="open-street-map",
        title="<b>King County Housing Map: Comps & Target Property Location</b>",
        hover_name="price",
        hover_data={
            "bedrooms": True,
            "bathrooms": True,
            "sqft_living": True,
            "grade": True,
            "zipcode": True,
            "lat": False,
            "long": False
        },
        opacity=0.6,
        height=580
    )

    # Highlight Target Property with prominent custom marker
    if target_lat is not None and target_lon is not None:
        price_text = f"${target_price:,.0f}" if target_price else "Estimated Valuation"
        hover_text = f"<b>📍 TARGET PROPERTY</b><br>Valuation: {price_text}<br>Lat: {target_lat:.4f}, Lon: {target_lon:.4f}"
        
        # Outer halo/pulse ring
        fig.add_trace(go.Scattermap(
            lat=[target_lat],
            lon=[target_lon],
            mode='markers',
            marker=dict(
                size=32,
                color='rgba(255, 0, 85, 0.35)',
                allowoverlap=True
            ),
            hoverinfo='skip',
            showlegend=False
        ))
        
        # Core glowing pin
        fig.add_trace(go.Scattermap(
            lat=[target_lat],
            lon=[target_lon],
            mode='markers+text',
            marker=dict(
                size=18,
                color='#E11D48',
                allowoverlap=True
            ),
            text=['📍 TARGET'],
            textposition='top center',
            textfont=dict(size=12, color='#9F1239', family='Inter, sans-serif'),
            name='Target Property',
            hoverinfo='text',
            hovertext=hover_text,
            showlegend=True
        ))

    fig.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        paper_bgcolor='white',
        coloraxis_colorbar=dict(
            title="Price ($)",
            tickformat="$,.0f",
            thickness=14,
            len=0.75,
            y=0.5
        )
    )
    return fig

# -------------------------------------------------------------
# 5. VISUALIZATION SECTION CHARTS (from Visualization.ipynb)
# -------------------------------------------------------------
def get_fig_map_overview():
    """Visualization 1: Real Map of King County Housing"""
    fig = px.scatter_map(
        df_sample_map,
        lat='lat',
        lon='long',
        color='price',
        size='sqft_living',
        color_continuous_scale='Viridis',
        range_color=[p1, p99],
        zoom=9,
        center=dict(lat=47.56, lon=-122.25),
        map_style="open-street-map",
        title="<b>Real Map: House Locations & Prices across King County (OpenStreetMap)</b>",
        hover_name="price",
        hover_data={"bedrooms": True, "bathrooms": True, "sqft_living": True, "grade": True, "zipcode": True},
        opacity=0.6,
        height=620
    )
    fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
    return fig

def get_fig_price_distribution():
    """Visualization 2: Raw Price vs Log Price Distribution"""
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=[
            f"Original Raw Price (Skewness: {df['price'].skew():.2f})", 
            f"Log-Transformed Price (Skewness: {df['log_price'].skew():.2f})"
        ]
    )
    fig.add_trace(
        go.Histogram(
            x=df['price'], 
            nbinsx=60, 
            marker_color='#2563eb', 
            name='Raw Price', 
            hovertemplate='Price: %{x:$,.0f}<br>Count: %{y}<extra></extra>'
        ), 
        row=1, col=1
    )
    fig.add_trace(
        go.Histogram(
            x=df['log_price'], 
            nbinsx=60, 
            marker_color='#ef4444', 
            name='Log(Price)',
            hovertemplate='Log Price: %{x:.2f}<br>Count: %{y}<extra></extra>'
        ), 
        row=1, col=2
    )
    fig.update_xaxes(title_text="Price ($)", row=1, col=1)
    fig.update_xaxes(title_text="Log(Price + 1)", row=1, col=2)
    fig.update_yaxes(title_text="Property Count", row=1, col=1)
    fig.update_yaxes(title_text="Property Count", row=1, col=2)
    fig.update_layout(
        template='plotly_white',
        title="<b>Price Distribution: Raw Skewness vs Log-Normalized Gaussian Curve</b>",
        showlegend=False,
        height=450,
        margin=dict(t=60, b=40, l=40, r=40)
    )
    return fig

def get_fig_living_vs_price():
    """Visualization 3: Living Area vs Price & Log Price with Trendlines"""
    sample = df_sample_viz
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=["Living Area vs Raw Price ($)", "Living Area vs Log Price (Linearized Fit)"]
    )
    
    # Scatter 1: Raw Price
    fig.add_trace(
        go.Scatter(
            x=sample['sqft_living'],
            y=sample['price'],
            mode='markers',
            marker=dict(
                color=sample['grade'],
                colorscale='Viridis',
                size=5,
                opacity=0.6,
                showscale=False
            ),
            name='Properties',
            hovertemplate='Sqft: %{x:,}<br>Price: %{y:$,.0f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Regression trendline for Raw Price
    m1, b1 = np.polyfit(df['sqft_living'], df['price'], 1)
    x_line = np.linspace(df['sqft_living'].min(), df['sqft_living'].max(), 100)
    fig.add_trace(
        go.Scatter(
            x=x_line, y=m1 * x_line + b1,
            mode='lines', line=dict(color='red', width=2.5, dash='dash'),
            name='OLS Linear Fit'
        ),
        row=1, col=1
    )

    # Scatter 2: Log Price
    fig.add_trace(
        go.Scatter(
            x=sample['sqft_living'],
            y=sample['log_price'],
            mode='markers',
            marker=dict(
                color=sample['grade'],
                colorscale='Viridis',
                size=5,
                opacity=0.6,
                colorbar=dict(title='Grade', x=1.02),
                showscale=True
            ),
            name='Properties (Log)',
            hovertemplate='Sqft: %{x:,}<br>Log Price: %{y:.2f}<extra></extra>'
        ),
        row=1, col=2
    )

    # Regression trendline for Log Price
    m2, b2 = np.polyfit(df['sqft_living'], df['log_price'], 1)
    fig.add_trace(
        go.Scatter(
            x=x_line, y=m2 * x_line + b2,
            mode='lines', line=dict(color='red', width=2.5, dash='dash'),
            name='OLS Log-Linear Fit'
        ),
        row=1, col=2
    )

    fig.update_xaxes(title_text="Living Area (sq ft)", row=1, col=1)
    fig.update_xaxes(title_text="Living Area (sq ft)", row=1, col=2)
    fig.update_yaxes(title_text="Price ($)", row=1, col=1)
    fig.update_yaxes(title_text="Log(Price)", row=1, col=2)
    fig.update_layout(
        template='plotly_white',
        title="<b>Living Area vs Price: Why Log Transformation Linearizes the Relationship</b>",
        showlegend=False,
        height=480,
        margin=dict(t=60, b=40, l=40, r=40)
    )
    return fig

def get_fig_lot_and_ratio():
    """Visualization 4: Living vs Lot Area (Log Scale) & Ratio vs Log Price"""
    sample = df_sample_viz
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=[
            "Living Area vs Lot Area (Log Scale) vs Price",
            "Living-to-Lot Ratio vs Log Price"
        ]
    )

    fig.add_trace(
        go.Scatter(
            x=sample['sqft_living'],
            y=sample['sqft_lot'],
            mode='markers',
            marker=dict(
                color=sample['price'],
                colorscale='Turbo',
                size=5,
                opacity=0.6,
                cmax=df['price'].quantile(0.98),
                colorbar=dict(title='Price ($)', x=0.46, tickformat='$,.0f')
            ),
            name='Lot vs Living',
            hovertemplate='Living: %{x:,} sqft<br>Lot: %{y:,} sqft<extra></extra>'
        ),
        row=1, col=1
    )
    fig.update_yaxes(type='log', title_text="Lot Area (sq ft - Log Scale)", row=1, col=1)
    fig.update_xaxes(title_text="Living Area (sq ft)", row=1, col=1)

    fig.add_trace(
        go.Scatter(
            x=sample['living_to_lot_ratio'],
            y=sample['log_price'],
            mode='markers',
            marker=dict(
                color=sample['grade'],
                colorscale='Magma',
                size=5,
                opacity=0.6,
                colorbar=dict(title='Grade', x=1.02)
            ),
            name='Ratio vs Price',
            hovertemplate='Ratio: %{x:.3f}<br>Log Price: %{y:.2f}<extra></extra>'
        ),
        row=1, col=2
    )
    fig.update_xaxes(title_text="Living-to-Lot Ratio", row=1, col=2)
    fig.update_yaxes(title_text="Log(Price)", row=1, col=2)

    fig.update_layout(
        template='plotly_white',
        title="<b>Lot Space & Density: Lot Area Analysis vs Living-to-Lot Ratio</b>",
        showlegend=False,
        height=480,
        margin=dict(t=60, b=40, l=40, r=40)
    )
    return fig

def get_fig_correlation_heatmap():
    """Visualization 5: Top Feature Correlations Heatmap"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    top_corr_cols = df[numeric_cols].corr()['price'].abs().nlargest(12).index
    corr_matrix = df[top_corr_cols].corr().round(2)

    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu_r',
        zmin=-1.0,
        zmax=1.0,
        text=corr_matrix.values,
        texttemplate="%{text:.2f}",
        textfont={"size": 10},
        hoverongaps=False
    ))
    fig.update_layout(
        template='plotly_white',
        title="<b>Correlation Matrix: Top 12 Numerical Predictors of House Price</b>",
        height=520,
        margin=dict(t=60, b=40, l=40, r=40)
    )
    return fig

def get_fig_grade_waterfront_boxplot():
    """Visualization 6: Construction Grade & Waterfront Status Impact"""
    fig = go.Figure()
    fig.add_trace(go.Box(
        x=df[df['waterfront'] == 0]['grade'],
        y=df[df['waterfront'] == 0]['price'],
        name='No Waterfront',
        marker_color='#2563eb',
        boxmean=True
    ))
    fig.add_trace(go.Box(
        x=df[df['waterfront'] == 1]['grade'],
        y=df[df['waterfront'] == 1]['price'],
        name='Waterfront Property 🌊',
        marker_color='#ef4444',
        boxmean=True
    ))
    fig.update_layout(
        boxmode='group',
        yaxis_type='log',
        template='plotly_white',
        title="<b>Price vs Construction Grade & Waterfront Status (Log Scale)</b>",
        xaxis_title="Construction Grade (1 = Cabins/Substandard, 7 = Average, 13 = Custom Luxury Mansions)",
        yaxis_title="Price ($ - Log Scale)",
        yaxis=dict(tickformat="$,.0f"),
        height=480,
        legend=dict(x=0.02, y=0.98),
        margin=dict(t=60, b=40, l=40, r=40)
    )
    return fig

def get_fig_spatial_density():
    """Visualization 7: Spatial Sales Density & Mean Geographic Price"""
    sample = df_sample_viz
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=[
            "Sales Volume Spatial Density (Seattle & Eastside Hubs)",
            "Average Log Price by Geographic Location"
        ]
    )
    # Hexbin-style 2D Histogram Density
    fig.add_trace(
        go.Histogram2d(
            x=df['long'],
            y=df['lat'],
            nbinsx=45,
            nbinsy=45,
            colorscale='Blues',
            colorbar=dict(title='Count', x=0.46)
        ),
        row=1, col=1
    )
    fig.update_xaxes(title_text="Longitude", row=1, col=1)
    fig.update_yaxes(title_text="Latitude", row=1, col=1)

    # Geographic scatter colored by Log Price
    fig.add_trace(
        go.Scatter(
            x=sample['long'],
            y=sample['lat'],
            mode='markers',
            marker=dict(
                color=sample['log_price'],
                colorscale='YlOrRd',
                size=4.5,
                opacity=0.7,
                colorbar=dict(title='Log(Price)', x=1.02)
            ),
            name='Spatial Price',
            hovertemplate='Lat: %{y:.3f}<br>Lon: %{x:.3f}<br>Log Price: %{marker.color:.2f}<extra></extra>'
        ),
        row=1, col=2
    )
    fig.update_xaxes(title_text="Longitude", row=1, col=2)
    fig.update_yaxes(title_text="Latitude", row=1, col=2)

    fig.update_layout(
        template='plotly_white',
        title="<b>Geospatial Intelligence: Sales Density Clusters vs Premium Geographic Hotspots</b>",
        showlegend=False,
        height=480,
        margin=dict(t=60, b=40, l=40, r=40)
    )
    return fig

def get_fig_3d_surface():
    """Visualization 8: 3D Surface Explorer (Living Area vs Grade vs Log Price)"""
    sample_3d = df.sample(n=min(3000, len(df)), random_state=42)
    fig = px.scatter_3d(
        sample_3d,
        x='sqft_living',
        y='grade',
        z='log_price',
        color='price_per_sqft',
        color_continuous_scale='Plasma',
        opacity=0.7,
        title="<b>3D Surface Explorer: Living Area vs Grade vs Log Price (Color: Price/Sqft)</b>",
        labels={
            'sqft_living': 'Living Area (sq ft)',
            'grade': 'Grade (1-13)',
            'log_price': 'Log(Price)',
            'price_per_sqft': '$/Sq Ft'
        },
        height=620
    )
    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=40),
        scene=dict(
            xaxis_title='Living Area',
            yaxis_title='Grade',
            zaxis_title='Log(Price)'
        )
    )
    return fig

def get_fig_zipcode_prices():
    """Visualization 9: Top 15 Most Expensive vs Top 15 Most Affordable Zipcodes"""
    zip_summary = df.groupby('zipcode').agg(
        median_price=('price', 'median'),
        mean_price=('price', 'mean'),
        count=('price', 'count')
    ).reset_index()

    top15 = zip_summary.sort_values(by='median_price', ascending=True).tail(15)
    bottom15 = zip_summary.sort_values(by='median_price', ascending=False).tail(15)

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=[
            "Top 15 Most Expensive Zipcodes (Median Price)",
            "Top 15 Most Affordable Zipcodes (Median Price)"
        ]
    )

    fig.add_trace(
        go.Bar(
            y=top15['zipcode'].astype(str),
            x=top15['median_price'],
            orientation='h',
            marker=dict(color=top15['median_price'], colorscale='Magma'),
            text=[f"${v:,.0f}" for v in top15['median_price']],
            textposition='outside',
            cliponaxis=False,
            name='Expensive Zipcodes',
            hovertemplate='<b>Zipcode %{y}</b><br>Median Price: %{x:$,.0f}<extra></extra>'
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(
            y=bottom15['zipcode'].astype(str),
            x=bottom15['median_price'],
            orientation='h',
            marker=dict(color=bottom15['median_price'], colorscale='Tealgrn'),
            text=[f"${v:,.0f}" for v in bottom15['median_price']],
            textposition='outside',
            cliponaxis=False,
            name='Affordable Zipcodes',
            hovertemplate='<b>Zipcode %{y}</b><br>Median Price: %{x:$,.0f}<extra></extra>'
        ),
        row=1, col=2
    )

    fig.update_xaxes(title_text="Median Price ($)", tickformat="$,.0f", row=1, col=1)
    fig.update_xaxes(title_text="Median Price ($)", tickformat="$,.0f", row=1, col=2)
    fig.update_yaxes(title_text="Postal Zipcode", row=1, col=1)
    fig.update_yaxes(title_text="Postal Zipcode", row=1, col=2)

    fig.update_layout(
        template='plotly_white',
        title="<b>Geographic Price Disparity: Top 15 Most Expensive vs Most Affordable King County Zipcodes</b>",
        showlegend=False,
        height=540,
        margin=dict(t=60, b=40, l=60, r=40)
    )
    return fig


# -------------------------------------------------------------
# 6. MACHINE LEARNING SECTION CHARTS (from MachineLearning.ipynb)
# -------------------------------------------------------------
def get_fig_ml_r2_comparison():
    """ML Bar Chart 1: R2 Score Comparison across Models"""
    fig = go.Figure(go.Bar(
        x=MODEL_COMPARISON['Model'],
        y=MODEL_COMPARISON['R2 Score'],
        marker_color=['#10b981', '#3b82f6', '#f59e0b', '#64748b'],
        text=[f"{val:.4f} ({val*100:.1f}%)" for val in MODEL_COMPARISON['R2 Score']],
        textposition='outside',
        cliponaxis=False
    ))
    fig.update_layout(
        template='plotly_white',
        title="<b>Model Accuracy Comparison: R² Score (Higher is Better)</b>",
        yaxis=dict(range=[0.70, 0.96], title="R² Score"),
        xaxis_title="Machine Learning Algorithm",
        height=380,
        margin=dict(t=50, b=40, l=40, r=40)
    )
    return fig

def get_fig_ml_mae_comparison():
    """ML Bar Chart 2: MAE Comparison across Models"""
    fig = go.Figure(go.Bar(
        x=MODEL_COMPARISON['Model'],
        y=MODEL_COMPARISON['MAE ($)'],
        marker_color=['#10b981', '#3b82f6', '#f59e0b', '#ef4444'],
        text=[f"${val:,.0f}" for val in MODEL_COMPARISON['MAE ($)']],
        textposition='outside',
        cliponaxis=False
    ))
    fig.update_layout(
        template='plotly_white',
        title="<b>Mean Absolute Error in $ (Lower is Better)</b>",
        yaxis=dict(title="MAE ($)", tickformat="$,.0f"),
        xaxis_title="Machine Learning Algorithm",
        height=380,
        margin=dict(t=50, b=40, l=40, r=40)
    )
    return fig

def get_fig_ml_actual_vs_predicted():
    """ML Scatter Plot: Actual vs Predicted Price for XGBoost on Test Set"""
    sample_eval = test_df.sample(n=min(1500, len(test_df)), random_state=42)
    fig = go.Figure()

    # Scatter points
    fig.add_trace(go.Scatter(
        x=sample_eval['Actual_Price'],
        y=sample_eval['Predicted_Price'],
        mode='markers',
        marker=dict(
            color='#1e40af',
            size=5.5,
            opacity=0.45
        ),
        name='Test Predictions',
        hovertemplate='Actual: %{x:$,.0f}<br>Predicted: %{y:$,.0f}<extra></extra>'
    ))

    # Perfect prediction line (y = x)
    min_val = min(test_df['Actual_Price'].min(), test_df['Predicted_Price'].min())
    max_val = max(test_df['Actual_Price'].max(), test_df['Predicted_Price'].max())
    fig.add_trace(go.Scatter(
        x=[min_val, max_val],
        y=[min_val, max_val],
        mode='lines',
        line=dict(color='#ef4444', width=2.5, dash='dash'),
        name='Ideal Identity (y = x)'
    ))

    fig.update_xaxes(type='log', title_text="Actual House Price ($ - Log Scale)", tickformat="$,.0f")
    fig.update_yaxes(type='log', title_text="Predicted House Price ($ - Log Scale)", tickformat="$,.0f")
    fig.update_layout(
        template='plotly_white',
        title="<b>Actual vs Predicted Price (XGBoost Regressor - Test Set)</b>",
        legend=dict(x=0.03, y=0.97),
        height=450,
        margin=dict(t=50, b=40, l=40, r=40)
    )
    return fig

def get_fig_ml_feature_importance():
    """ML Bar Chart: Feature Importance for XGBoost"""
    top_fi = feature_importances.head(12).sort_values(by='Importance', ascending=True)
    fig = go.Figure(go.Bar(
        x=top_fi['Importance'],
        y=top_fi['Feature_Label'],
        orientation='h',
        marker=dict(
            color=top_fi['Importance'],
            colorscale='Tealgrn'
        ),
        text=[f"{val*100:.1f}%" for val in top_fi['Importance']],
        textposition='outside',
        cliponaxis=False
    ))
    fig.update_layout(
        template='plotly_white',
        title="<b>XGBoost Feature Importance: Top Drivers of House Valuation</b>",
        xaxis_title="Relative Feature Importance",
        yaxis_title="",
        height=450,
        margin=dict(t=50, b=40, l=180, r=50)
    )
    return fig

def get_fig_ml_residuals():
    """ML Error Distribution: Residuals Histogram"""
    fig = go.Figure(go.Histogram(
        x=test_df['Residual'],
        nbinsx=60,
        marker_color='#8b5cf6',
        name='Residuals',
        hovertemplate='Residual: %{x:$,.0f}<br>Count: %{y}<extra></extra>'
    ))
    fig.add_vline(x=0, line_width=2, line_dash="dash", line_color="red")
    fig.update_layout(
        template='plotly_white',
        title="<b>Residual Error Distribution (Actual - Predicted) Centered at $0</b>",
        xaxis=dict(title="Error ($)", range=[-300000, 300000], tickformat="$,.0f"),
        yaxis_title="Frequency",
        height=380,
        margin=dict(t=50, b=40, l=40, r=40)
    )
    return fig

