"""
app.py
Main Plotly Dash application for King County Real Estate Valuation.
This file connects the layouts, handles user interactions, and runs the web app.
"""

import dash
from dash import dcc, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc

import data_loader as dl
from layouts import (
    get_header,
    get_kpi_banner,
    get_prediction_tab,
    get_visualizations_tab,
    get_ml_tab,
    get_dataset_tab,
    get_footer
)

# -----------------------------------------------------------------------------
# 1. INITIALIZE DASH APPLICATION
# -----------------------------------------------------------------------------
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css"
    ],
    title="King County Real Estate Valuation | Price Prediction & Analytics",
    suppress_callback_exceptions=True
)
server = app.server

# -----------------------------------------------------------------------------
# 2. ASSEMBLE MASTER LAYOUT (All HTML/CSS components live in layouts/)
# -----------------------------------------------------------------------------
app.layout = html.Div([
    get_header(),
    get_kpi_banner(),
    
    dbc.Container(
        fluid=True,
        className="mb-4",
        children=[
            dbc.Tabs(
                id="app-tabs",
                active_tab="tab-predict",
                className="nav-tabs mb-4",
                children=[
                    dbc.Tab(label="🔮 Price Prediction & Location Map", tab_id="tab-predict", children=get_prediction_tab()),
                    dbc.Tab(label="📊 Exploratory Visualizations", tab_id="tab-visualizations", children=get_visualizations_tab()),
                    dbc.Tab(label="🤖 Machine Learning & Why XGBoost", tab_id="tab-ml", children=get_ml_tab()),
                    dbc.Tab(label="📁 Dataset Explorer & Dictionary", tab_id="tab-dataset", children=get_dataset_tab()),
                ]
            )
        ]
    ),
    
    get_footer()
])

# -----------------------------------------------------------------------------
# 3. INTERACTIVE CALLBACKS
# -----------------------------------------------------------------------------

# Callback A: Sync quick test presets, zipcode selection, and map clicks
@app.callback(
    Output("input-bedrooms", "value"),
    Output("input-bathrooms", "value"),
    Output("input-sqft-living", "value"),
    Output("input-sqft-lot", "value"),
    Output("input-floors", "value"),
    Output("input-has-basement", "value"),
    Output("input-grade", "value"),
    Output("input-condition", "value"),
    Output("input-view", "value"),
    Output("input-waterfront", "value"),
    Output("input-zipcode", "value"),
    Output("input-lat", "value"),
    Output("input-long", "value"),
    Output("input-yr-built", "value"),
    Output("input-is-renovated", "value"),
    Output("input-yr-renovated", "value"),
    Output("input-sqft-living15", "value"),
    Output("input-sqft-lot15", "value"),
    Input("preset-standard", "n_clicks"),
    Input("preset-luxury", "n_clicks"),
    Input("preset-waterfront", "n_clicks"),
    Input("preset-suburban", "n_clicks"),
    Input("input-zipcode", "value"),
    Input("main-map", "clickData"),
    State("input-bedrooms", "value"),
    State("input-bathrooms", "value"),
    State("input-sqft-living", "value"),
    State("input-sqft-lot", "value"),
    State("input-floors", "value"),
    State("input-has-basement", "value"),
    State("input-grade", "value"),
    State("input-condition", "value"),
    State("input-view", "value"),
    State("input-waterfront", "value"),
    State("input-lat", "value"),
    State("input-long", "value"),
    State("input-yr-built", "value"),
    State("input-is-renovated", "value"),
    State("input-yr-renovated", "value"),
    State("input-sqft-living15", "value"),
    State("input-sqft-lot15", "value"),
    prevent_initial_call=True
)
def handle_presets_and_clicks(
    n_std, n_lux, n_wat, n_sub, zip_val, click_data,
    bed, bath, sqft, lot, floors, base, grade, cond, view, wf,
    lat, lon, yr_built, is_renov, yr_renov, liv15, lot15
):
    """Updates the input boxes when presets are clicked, zipcode is changed, or the map is clicked."""
    trigger = ctx.triggered_id

    # Preset 1: Seattle Standard Home
    if trigger == "preset-standard":
        return 3, 2.0, 1800, 5000, "1.5", "0", "7", "3", "0", "0", 98103, 47.67, -122.34, 1975, "0", 0, 1800, 5000

    # Preset 2: Bellevue Luxury Mansion
    elif trigger == "preset-luxury":
        return 5, 4.5, 4800, 12000, "2.0", "1", "11", "4", "2", "0", 98004, 47.616, -122.205, 2008, "0", 0, 4200, 11000

    # Preset 3: Mercer Island Waterfront Estate
    elif trigger == "preset-waterfront":
        return 4, 4.0, 4200, 16000, "2.0", "1", "12", "4", "4", "1", 98040, 47.575, -122.228, 1995, "1", 2012, 3800, 15000

    # Preset 4: Suburban Family Home
    elif trigger == "preset-suburban":
        return 3, 1.75, 1500, 8000, "1.0", "0", "7", "3", "0", "0", 98001, 47.309, -122.271, 1980, "0", 0, 1600, 7800

    # Zipcode changed -> automatically set center coordinates of that zipcode
    elif trigger == "input-zipcode" and zip_val in dl.zip_coords:
        new_lat = dl.zip_coords[zip_val]['lat']
        new_lon = dl.zip_coords[zip_val]['long']
        return bed, bath, sqft, lot, floors, base, grade, cond, view, wf, zip_val, new_lat, new_lon, yr_built, is_renov, yr_renov, liv15, lot15

    # Map clicked -> update coordinates and find nearest zipcode
    elif trigger == "main-map" and click_data:
        pt = click_data['points'][0]
        new_lat = round(pt['lat'], 4)
        new_lon = round(pt['lon'], 4)
        nearest_zip = dl.find_nearest_zipcode(new_lat, new_lon)
        return bed, bath, sqft, lot, floors, base, grade, cond, view, wf, nearest_zip, new_lat, new_lon, yr_built, is_renov, yr_renov, liv15, lot15

    return bed, bath, sqft, lot, floors, base, grade, cond, view, wf, zip_val, lat, lon, yr_built, is_renov, yr_renov, liv15, lot15


# Callback B: Calculate Valuation with XGBoost and update the map pin
@app.callback(
    Output("predicted-price-display", "children"),
    Output("confidence-range-display", "children"),
    Output("tier-badge", "children"),
    Output("tier-badge", "className"),
    Output("stat-price-per-sqft", "children"),
    Output("stat-ratio", "children"),
    Output("stat-age", "children"),
    Output("stat-renovated", "children"),
    Output("main-map", "figure"),
    Input("btn-recalculate", "n_clicks"),
    Input("input-bedrooms", "value"),
    Input("input-bathrooms", "value"),
    Input("input-sqft-living", "value"),
    Input("input-sqft-lot", "value"),
    Input("input-floors", "value"),
    Input("input-has-basement", "value"),
    Input("input-grade", "value"),
    Input("input-condition", "value"),
    Input("input-view", "value"),
    Input("input-waterfront", "value"),
    Input("input-zipcode", "value"),
    Input("input-lat", "value"),
    Input("input-long", "value"),
    Input("input-yr-built", "value"),
    Input("input-is-renovated", "value"),
    Input("input-yr-renovated", "value"),
    Input("input-sqft-living15", "value"),
    Input("input-sqft-lot15", "value"),
    Input("map-max-price", "value"),
    Input("map-waterfront-only", "value")
)
def update_valuation_and_map(
    n_calc, bedrooms, bathrooms, sqft_living, sqft_lot, floors, has_basement,
    grade, condition, view, waterfront, zipcode, lat, long,
    yr_built, is_renovated, yr_renovated, sqft_living15, sqft_lot15,
    max_price_filter, waterfront_only_flag
):
    """Feeds feature values into the XGBoost model and renders the valuation & map."""
    # Run the machine learning prediction
    pred = dl.predict_house_price(
        bedrooms=bedrooms or 3,
        bathrooms=bathrooms or 2.0,
        sqft_living=sqft_living or 2000,
        sqft_lot=sqft_lot or 7500,
        floors=float(floors or 1.5),
        waterfront=int(waterfront or 0),
        view=int(view or 0),
        condition=int(condition or 3),
        grade=int(grade or 7),
        zipcode=int(zipcode or 98103),
        lat=float(lat or 47.67),
        long=float(long or -122.34),
        sqft_living15=sqft_living15 or sqft_living or 2000,
        sqft_lot15=sqft_lot15 or sqft_lot or 7500,
        has_basement=int(has_basement or 0),
        yr_built=int(yr_built or 1985),
        is_renovated=int(is_renovated or 0),
        yr_renovated=int(yr_renovated or 0)
    )

    # Format numbers into clean currency strings
    price_formatted = f"${pred['predicted_price']:,.0f}"
    range_formatted = f"Confidence Range: ${pred['min_range']:,.0f} - ${pred['max_range']:,.0f} (+/- $64.6k MAE)"
    tier_text = pred['tier']
    tier_badge_class = f"badge bg-{pred['tier_color']} text-white fw-bold px-3 py-1"
    
    sqft_price_text = f"${pred['price_per_sqft']:.2f}"
    ratio_text = f"{pred['living_to_lot_ratio']:.2f}"
    age_text = f"{pred['house_age']} Years"
    renov_text = f"Yes ({pred['years_since_renovation']} yrs ago)" if int(is_renovated or 0) else "Original (None)"

    # Build the interactive map with highlighted pin
    is_waterfront_only = bool(waterfront_only_flag and len(waterfront_only_flag) > 0)
    map_fig = dl.build_main_map(
        target_lat=float(lat or 47.67),
        target_lon=float(long or -122.34),
        target_price=pred['predicted_price'],
        max_price_filter=float(max_price_filter or 2500000.0),
        waterfront_only=is_waterfront_only
    )

    return (
        price_formatted,
        range_formatted,
        tier_text,
        tier_badge_class,
        sqft_price_text,
        ratio_text,
        age_text,
        renov_text,
        map_fig
    )

# -----------------------------------------------------------------------------
# 4. ENTRYPOINT
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    print("=" * 65)
    print("  🚀 King County Real Estate Valuation Dashboard")
    print("  🌐 Running on: http://127.0.0.1:8050")
    print("=" * 65)
    app.run(debug=True, host='127.0.0.1', port=8050)
