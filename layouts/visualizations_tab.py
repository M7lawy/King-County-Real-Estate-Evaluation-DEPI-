"""
layouts/visualizations_tab.py
Layout for Tab 2: Exploratory Data Visualizations (from Visualization.ipynb).
"""

from dash import dcc, html
import dash_bootstrap_components as dbc
import data_loader as dl

def get_visualizations_tab():
    """Builds the visualizations tab with charts from Visualization.ipynb."""
    return dbc.Container(
        fluid=True,
        children=[
            # SECTION OVERVIEW
            html.Div(
                className="callout-info mb-4",
                children=[
                    html.H5("📊 Exploratory Data Analysis & Empirical Insights", className="fw-bold text-primary mb-1"),
                    html.P(
                        "This section showcases the comprehensive exploratory visualizations from Visualization.ipynb. "
                        "These charts reveal the strong price skewness, spatial micro-clustering, "
                        "exponential relationships with living space, and the massive valuation premium of waterfront and architectural grade.",
                        className="mb-0 text-secondary"
                    )
                ]
            ),

            # VIZ 1: REAL HOUSING MAP OVERVIEW
            html.Div(
                className="dashboard-card",
                children=[
                    html.H5("1. Real Map: House Locations & Price Distribution (King County)", className="card-title-custom"),
                    html.P("Geographic scatter map of 5,000 sampled transactions on OpenStreetMap. Bubble size encodes interior living square footage; color represents sale price ($175k to $1.96M quantile range).", className="text-muted small"),
                    dcc.Graph(figure=dl.get_fig_map_overview(), config={"scrollZoom": True})
                ]
            ),

            # VIZ 2: PRICE SKEWNESS & LOG-TRANSFORM
            html.Div(
                className="dashboard-card",
                children=[
                    html.H5("2. Price Skewness & The Power of Log Transformation", className="card-title-custom"),
                    html.P("Raw real estate prices exhibit extreme positive skewness (+4.02) with high-value luxury tails. Applying np.log1p(price) transforms the distribution into a near-normal Gaussian bell curve (+0.43 skewness), stabilizing variance and boosting ML regression performance.", className="text-muted small"),
                    dcc.Graph(figure=dl.get_fig_price_distribution())
                ]
            ),

            # VIZ 3: LIVING AREA VS PRICE & LOG PRICE
            html.Div(
                className="dashboard-card",
                children=[
                    html.H5("3. Living Area vs Raw Price vs Log Price (Linearized Fit)", className="card-title-custom"),
                    html.P("Comparing living square footage against raw price (left) reveals exponential fan-out heteroscedasticity. In contrast, plotting against log price (right) yields a tightly linearized relationship with consistent variance across all construction grades.", className="text-muted small"),
                    dcc.Graph(figure=dl.get_fig_living_vs_price())
                ]
            ),

            # VIZ 4: LOT SPACE & DENSITY RATIO
            html.Div(
                className="dashboard-card",
                children=[
                    html.H5("4. Lot Size Analysis & Living-to-Lot Space Ratio", className="card-title-custom"),
                    html.P("Left: Living Area vs Lot Area plotted on a logarithmic y-axis reveals the spread between compact urban parcels and vast suburban/rural acreage. Right: The engineered living_to_lot_ratio shows high-density urban properties commanding premium prices per land footprint.", className="text-muted small"),
                    dcc.Graph(figure=dl.get_fig_lot_and_ratio())
                ]
            ),

            # VIZ 5: CORRELATION HEATMAP
            html.Div(
                className="dashboard-card",
                children=[
                    html.H5("5. Correlation Matrix: Top 12 Numerical Predictors", className="card-title-custom"),
                    html.P("Pearson correlation coefficients between top numerical housing features and sale price. Construction Grade (+0.67), Living Area (+0.70), and Sqft Living of 15 Neighbors (+0.59) stand out as the strongest single linear drivers.", className="text-muted small"),
                    dcc.Graph(figure=dl.get_fig_correlation_heatmap())
                ]
            ),

            # VIZ 6: GRADE & WATERFRONT BOXPLOT
            html.Div(
                className="dashboard-card",
                children=[
                    html.H5("6. Price Distribution by Construction Grade & Waterfront Status (Log Scale)", className="card-title-custom"),
                    html.P("Log-scale boxplot demonstrating that waterfront properties (red) command an immense valuation premium over inland homes (blue) across every single construction grade tier (Grades 1 through 13).", className="text-muted small"),
                    dcc.Graph(figure=dl.get_fig_grade_waterfront_boxplot())
                ]
            ),

            # VIZ 7: GEOSPATIAL DENSITY & AVERAGE PRICE
            html.Div(
                className="dashboard-card",
                children=[
                    html.H5("7. Geospatial Intelligence: Transaction Density vs Price Clusters", className="card-title-custom"),
                    html.P("Left: Spatial density highlighting heavy transaction volume centered in Seattle and Bellevue. Right: Average log price mapped across coordinates showing clear geographical price clusters around Lake Washington, Mercer Island, and Medina.", className="text-muted small"),
                    dcc.Graph(figure=dl.get_fig_spatial_density())
                ]
            ),

            # VIZ 8: 3D SURFACE EXPLORER
            html.Div(
                className="dashboard-card",
                children=[
                    html.H5("8. 3D Surface Explorer: Living Area vs Grade vs Log Price", className="card-title-custom"),
                    html.P("Interactive 3D scatter plot (rotatable with mouse). Points are colored by Price Per Square Foot (Plasma colorscale), showing how high construction grade and square footage interact simultaneously to elevate property values.", className="text-muted small"),
                    dcc.Graph(figure=dl.get_fig_3d_surface())
                ]
            )
        ]
    )

