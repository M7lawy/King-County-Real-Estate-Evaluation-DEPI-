"""
layouts/prediction_tab.py
Layout for Tab 1 (Main Section): House Price Prediction & Interactive Map.
"""

from dash import dcc, html
import dash_bootstrap_components as dbc
import data_loader as dl

def get_prediction_tab():
    """Builds the main prediction tab containing feature inputs and map."""
    grade_options = [
        {"label": "1 - 3: Substandard / Low Grade Cabin", "value": 3},
        {"label": "4 - 6: Low to Below Average Construction", "value": 6},
        {"label": "7: Average Construction & Standard Quality", "value": 7},
        {"label": "8: Good Construction & Architectural Details", "value": 8},
        {"label": "9: Better Quality Finishes & Design", "value": 9},
        {"label": "10: Very Good Custom Quality", "value": 10},
        {"label": "11: Excellent Luxury Craftsmanship", "value": 11},
        {"label": "12: High Luxury / Custom Architecture", "value": 12},
        {"label": "13: Top-Tier Mansion / World-Class Estate", "value": 13},
    ]

    zip_options = [{"label": f"{z} (King County)", "value": z} for z in dl.zipcode_list]

    return dbc.Container(
        fluid=True,
        children=[
            dbc.Row(
                className="g-4",
                children=[
                    # LEFT COLUMN: FEATURE INPUTS FORM
                    dbc.Col(
                        lg=5, xl=5,
                        children=[
                            html.Div(
                                className="dashboard-card",
                                children=[
                                    html.Div(
                                        className="card-title-custom",
                                        children=[
                                            html.I(className="bi bi-sliders text-primary fs-5"),
                                            html.Span("Property Characteristics & Feature Inputs")
                                        ]
                                    ),
                                    
                                    # QUICK PRESETS
                                    html.Div(
                                        className="mb-3 p-2 bg-light rounded border",
                                        children=[
                                            html.Small("⚡ Quick Test Presets:", className="d-block fw-bold text-muted mb-2"),
                                            html.Div(
                                                className="d-flex flex-wrap",
                                                children=[
                                                    html.Button("🏡 Seattle Standard", id="preset-standard", className="btn btn-preset", n_clicks=0),
                                                    html.Button("💎 Bellevue Luxury", id="preset-luxury", className="btn btn-preset", n_clicks=0),
                                                    html.Button("🌊 Mercer Waterfront", id="preset-waterfront", className="btn btn-preset", n_clicks=0),
                                                    html.Button("🌲 Suburban Family", id="preset-suburban", className="btn btn-preset", n_clicks=0),
                                                ]
                                            )
                                        ]
                                    ),

                                    # 1. CORE DIMENSIONS
                                    html.H6("1. Living Space & Rooms", className="fw-bold text-secondary mb-2 mt-3"),
                                    dbc.Row(
                                        className="g-2 mb-2",
                                        children=[
                                            dbc.Col(
                                                sm=6,
                                                children=[
                                                    html.Label("Bedrooms", className="form-label"),
                                                    dbc.Input(id="input-bedrooms", type="number", min=1, max=15, step=1, value=3)
                                                ]
                                            ),
                                            dbc.Col(
                                                sm=6,
                                                children=[
                                                    html.Label("Bathrooms", className="form-label"),
                                                    dbc.Input(id="input-bathrooms", type="number", min=0.5, max=8.0, step=0.25, value=2.25)
                                                ]
                                            ),
                                        ]
                                    ),
                                    dbc.Row(
                                        className="g-2 mb-2",
                                        children=[
                                            dbc.Col(
                                                sm=6,
                                                children=[
                                                    html.Label("Interior Area (sq ft)", className="form-label"),
                                                    dbc.Input(id="input-sqft-living", type="number", min=300, max=15000, step=50, value=2000)
                                                ]
                                            ),
                                            dbc.Col(
                                                sm=6,
                                                children=[
                                                    html.Label("Lot Area (sq ft)", className="form-label"),
                                                    dbc.Input(id="input-sqft-lot", type="number", min=500, max=1000000, step=100, value=7500)
                                                ]
                                            ),
                                        ]
                                    ),
                                    dbc.Row(
                                        className="g-2 mb-3",
                                        children=[
                                            dbc.Col(
                                                sm=6,
                                                children=[
                                                    html.Label("Floors", className="form-label"),
                                                    dbc.Select(
                                                        id="input-floors",
                                                        options=[{"label": f"{fl} Floors", "value": fl} for fl in [1.0, 1.5, 2.0, 2.5, 3.0, 3.5]],
                                                        value="1.5"
                                                    )
                                                ]
                                            ),
                                            dbc.Col(
                                                sm=6,
                                                children=[
                                                    html.Label("Basement Present?", className="form-label"),
                                                    dbc.Select(
                                                        id="input-has-basement",
                                                        options=[{"label": "No Basement", "value": 0}, {"label": "Yes, Has Basement", "value": 1}],
                                                        value="0"
                                                    )
                                                ]
                                            ),
                                        ]
                                    ),

                                    # 2. QUALITY, VIEW & CONDITION
                                    html.H6("2. Quality, Condition & View", className="fw-bold text-secondary mb-2 mt-3"),
                                    html.Div(
                                        className="mb-2",
                                        children=[
                                            html.Label("Construction Grade (1-13)", className="form-label"),
                                            dbc.Select(
                                                id="input-grade",
                                                options=grade_options,
                                                value="7"
                                            )
                                        ]
                                    ),
                                    dbc.Row(
                                        className="g-2 mb-3",
                                        children=[
                                            dbc.Col(
                                                sm=4,
                                                children=[
                                                    html.Label("Condition (1-5)", className="form-label"),
                                                    dbc.Select(
                                                        id="input-condition",
                                                        options=[
                                                            {"label": "1 - Poor", "value": 1},
                                                            {"label": "2 - Fair", "value": 2},
                                                            {"label": "3 - Average", "value": 3},
                                                            {"label": "4 - Good", "value": 4},
                                                            {"label": "5 - Very Good", "value": 5},
                                                        ],
                                                        value="3"
                                                    )
                                                ]
                                            ),
                                            dbc.Col(
                                                sm=4,
                                                children=[
                                                    html.Label("View Quality (0-4)", className="form-label"),
                                                    dbc.Select(
                                                        id="input-view",
                                                        options=[
                                                            {"label": "0 - None", "value": 0},
                                                            {"label": "1 - Fair", "value": 1},
                                                            {"label": "2 - Average", "value": 2},
                                                            {"label": "3 - Good", "value": 3},
                                                            {"label": "4 - Spectacular", "value": 4},
                                                        ],
                                                        value="0"
                                                    )
                                                ]
                                            ),
                                            dbc.Col(
                                                sm=4,
                                                children=[
                                                    html.Label("Waterfront?", className="form-label"),
                                                    dbc.Select(
                                                        id="input-waterfront",
                                                        options=[{"label": "No", "value": 0}, {"label": "Yes 🌊", "value": 1}],
                                                        value="0"
                                                    )
                                                ]
                                            ),
                                        ]
                                    ),

                                    # 3. LOCATION & COORDINATES
                                    html.H6("3. Geographic Location & Coordinates", className="fw-bold text-secondary mb-2 mt-3"),
                                    html.Div(
                                        className="mb-2",
                                        children=[
                                            html.Label("Zipcode Area", className="form-label"),
                                            dcc.Dropdown(
                                                id="input-zipcode",
                                                options=zip_options,
                                                value=98103,
                                                clearable=False,
                                                style={"fontSize": "0.9rem"}
                                            )
                                        ]
                                    ),
                                    dbc.Row(
                                        className="g-2 mb-2",
                                        children=[
                                            dbc.Col(
                                                sm=6,
                                                children=[
                                                    html.Label("Latitude", className="form-label"),
                                                    dbc.Input(id="input-lat", type="number", step=0.0001, value=47.67)
                                                ]
                                            ),
                                            dbc.Col(
                                                sm=6,
                                                children=[
                                                    html.Label("Longitude", className="form-label"),
                                                    dbc.Input(id="input-long", type="number", step=0.0001, value=-122.34)
                                                ]
                                            ),
                                        ]
                                    ),
                                    html.Small(
                                        [html.I(className="bi bi-geo-alt-fill text-danger me-1"), "Tip: You can also click directly anywhere on the map to set coordinates!"],
                                        className="text-muted d-block mb-3"
                                    ),

                                    # 4. AGE & RENOVATIONS
                                    html.H6("4. Age, Renovation & Neighborhood Comps", className="fw-bold text-secondary mb-2 mt-3"),
                                    dbc.Row(
                                        className="g-2 mb-2",
                                        children=[
                                            dbc.Col(
                                                sm=4,
                                                children=[
                                                    html.Label("Year Built", className="form-label"),
                                                    dbc.Input(id="input-yr-built", type="number", min=1900, max=2024, step=1, value=1985)
                                                ]
                                            ),
                                            dbc.Col(
                                                sm=4,
                                                children=[
                                                    html.Label("Renovated?", className="form-label"),
                                                    dbc.Select(
                                                        id="input-is-renovated",
                                                        options=[{"label": "No", "value": 0}, {"label": "Yes", "value": 1}],
                                                        value="0"
                                                    )
                                                ]
                                            ),
                                            dbc.Col(
                                                sm=4,
                                                children=[
                                                    html.Label("Year Renovated", className="form-label"),
                                                    dbc.Input(id="input-yr-renovated", type="number", min=1930, max=2024, step=1, value=0)
                                                ]
                                            ),
                                        ]
                                    ),
                                    dbc.Row(
                                        className="g-2 mb-3",
                                        children=[
                                            dbc.Col(
                                                sm=6,
                                                children=[
                                                    html.Label("Neighbors Living Area (sqft)", className="form-label"),
                                                    dbc.Input(id="input-sqft-living15", type="number", min=300, max=10000, step=50, value=2000)
                                                ]
                                            ),
                                            dbc.Col(
                                                sm=6,
                                                children=[
                                                    html.Label("Neighbors Lot Area (sqft)", className="form-label"),
                                                    dbc.Input(id="input-sqft-lot15", type="number", min=500, max=500000, step=100, value=7500)
                                                ]
                                            ),
                                        ]
                                    ),

                                    # RECALCULATE ACTION BUTTON
                                    html.Div(
                                        className="d-grid mt-4",
                                        children=[
                                            dbc.Button(
                                                [html.I(className="bi bi-calculator me-2"), "Recalculate Valuation"],
                                                id="btn-recalculate",
                                                color="primary",
                                                size="lg",
                                                className="btn-primary-action"
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),

                    # RIGHT COLUMN: VALUATION RESULT & INTERACTIVE MAP
                    dbc.Col(
                        lg=7, xl=7,
                        children=[
                            # VALUATION RESULT CARD
                            html.Div(
                                id="valuation-result-container",
                                className="valuation-result-box",
                                children=[
                                    html.Div(
                                        className="d-flex justify-content-between align-items-center mb-1",
                                        children=[
                                            html.Span([html.I(className="bi bi-shield-check text-info me-1"), "Market Estimate (XGBoost)"], className="text-light fw-bold small text-uppercase"),
                                            html.Span(id="tier-badge", className="badge bg-light text-dark fw-bold px-3 py-1")
                                        ]
                                    ),
                                    html.Div(id="predicted-price-display", className="valuation-amount", children="$633,091"),
                                    html.Div(id="confidence-range-display", className="valuation-range mb-3", children="Confidence Range: $568,492 - $697,691 (+/- $64,599 MAE)"),
                                    
                                    # SUB METRIC CHIPS
                                    dbc.Row(
                                        className="g-2 text-start pt-2 border-top border-white border-opacity-25",
                                        children=[
                                            dbc.Col(
                                                sm=3, xs=6,
                                                children=html.Div([
                                                    html.Small("Price / Sq Ft", className="text-white-50 d-block"),
                                                    html.Strong(id="stat-price-per-sqft", children="$316.55", className="text-white")
                                                ])
                                            ),
                                            dbc.Col(
                                                sm=3, xs=6,
                                                children=html.Div([
                                                    html.Small("Living/Lot Ratio", className="text-white-50 d-block"),
                                                    html.Strong(id="stat-ratio", children="0.27", className="text-white")
                                                ])
                                            ),
                                            dbc.Col(
                                                sm=3, xs=6,
                                                children=html.Div([
                                                    html.Small("Property Age", className="text-white-50 d-block"),
                                                    html.Strong(id="stat-age", children="30 Years", className="text-white")
                                                ])
                                            ),
                                            dbc.Col(
                                                sm=3, xs=6,
                                                children=html.Div([
                                                    html.Small("Renovation Status", className="text-white-50 d-block"),
                                                    html.Strong(id="stat-renovated", children="Original (None)", className="text-white")
                                                ])
                                            ),
                                        ]
                                    )
                                ]
                            ),

                            # INTERACTIVE MAP CARD
                            html.Div(
                                className="dashboard-card p-3",
                                children=[
                                    html.Div(
                                        className="d-flex justify-content-between align-items-center mb-2 pb-2 border-bottom",
                                        children=[
                                            html.Div(
                                                className="d-flex align-items-center gap-2",
                                                children=[
                                                    html.I(className="bi bi-map-fill text-danger fs-5"),
                                                    html.H5("King County Location & Comparables Map", className="mb-0 fw-bold")
                                                ]
                                            ),
                                            html.Span([
                                                html.I(className="bi bi-geo-alt-fill text-danger me-1"),
                                                html.Small("Target House Highlighted with Crimson Pin", className="text-muted fw-semibold")
                                            ])
                                        ]
                                    ),
                                    
                                    # MAP FILTERS
                                    dbc.Row(
                                        className="g-2 mb-2 align-items-center px-1",
                                        children=[
                                            dbc.Col(
                                                md=8,
                                                children=[
                                                    html.Small("Filter Comps by Max Price: ", className="text-muted fw-bold me-2"),
                                                    dcc.Slider(
                                                        id="map-max-price",
                                                        min=300000,
                                                        max=3000000,
                                                        step=100000,
                                                        value=2500000,
                                                        marks={
                                                            500000: "$500k",
                                                            1000000: "$1M",
                                                            1500000: "$1.5M",
                                                            2000000: "$2M",
                                                            2500000: "$2.5M+"
                                                        },
                                                        tooltip={"placement": "bottom", "always_visible": False}
                                                    )
                                                ]
                                            ),
                                            dbc.Col(
                                                md=4,
                                                className="text-end",
                                                children=[
                                                    dbc.Checklist(
                                                        id="map-waterfront-only",
                                                        options=[{"label": " Waterfront Comps Only", "value": 1}],
                                                        value=[],
                                                        switch=True,
                                                        className="d-inline-block small"
                                                    )
                                                ]
                                            )
                                        ]
                                    ),

                                    # GRAPH MAP
                                    dcc.Loading(
                                        type="circle",
                                        color="#2563eb",
                                        children=dcc.Graph(
                                            id="main-map",
                                            config={"scrollZoom": True, "displayModeBar": True},
                                            style={"borderRadius": "0.5rem", "overflow": "hidden"}
                                        )
                                    ),
                                    
                                    html.Div(
                                        className="d-flex justify-content-between align-items-center mt-2 px-1 text-muted small",
                                        children=[
                                            html.Span([
                                                html.I(className="bi bi-cursor-fill text-primary me-1"),
                                                "Click any comp or location on the map to relocate target property!"
                                            ]),
                                            html.Span([
                                                html.I(className="bi bi-layers-fill text-secondary me-1"),
                                                "OpenStreetMap Vector Basemap"
                                            ])
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )

