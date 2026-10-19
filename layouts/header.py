"""
layouts/header.py
Header bar and top KPI metric summary cards for the dashboard.
"""

from dash import html
import dash_bootstrap_components as dbc
import data_loader as dl

def get_header():
    """Returns the top navigation banner without 'AI' in the title."""
    return html.Div(
        className="app-header",
        children=[
            dbc.Container(
                fluid=True,
                children=[
                    dbc.Row(
                        className="align-items-center",
                        children=[
                            dbc.Col(
                                md=7,
                                children=[
                                    html.Div(
                                        className="d-flex align-items-center gap-3",
                                        children=[
                                            html.Div(
                                                html.I(className="bi bi-houses-fill fs-1 text-info"),
                                                className="p-2 rounded-3 bg-dark bg-opacity-50"
                                            ),
                                            html.Div([
                                                # Site title without 'AI'
                                                html.H1("King County Real Estate Valuation", className="brand-title mb-0"),
                                                html.P("Property Price Prediction & Housing Analytics Hub | Washington State", className="brand-subtitle")
                                            ])
                                        ]
                                    )
                                ]
                            ),
                            dbc.Col(
                                md=5,
                                className="text-md-end mt-3 mt-md-0",
                                children=[
                                    html.Span([
                                        html.I(className="bi bi-cpu-fill text-warning me-1"),
                                        "Model: ", html.Strong("XGBoost Regressor (R² = 90.98%)", className="text-light me-3")
                                    ]),
                                    html.Span([
                                        html.I(className="bi bi-database-check text-success me-1"),
                                        "Sample: ", html.Strong("21,612 Homes", className="text-light")
                                    ])
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )

def get_kpi_banner():
    """Returns the 4 summary metric KPI cards."""
    return dbc.Container(
        fluid=True,
        className="my-3",
        children=[
            dbc.Row(
                className="g-3",
                children=[
                    dbc.Col(
                        sm=6, md=3,
                        children=html.Div(
                            className="kpi-card",
                            children=[
                                html.P("Dataset Transactions", className="kpi-label"),
                                html.Div(f"{len(dl.df):,}", className="kpi-value text-primary"),
                                html.Small("King County Sales (2014-2015)", className="text-muted")
                            ]
                        )
                    ),
                    dbc.Col(
                        sm=6, md=3,
                        children=html.Div(
                            className="kpi-card",
                            children=[
                                html.P("Median House Price", className="kpi-label"),
                                html.Div(f"${dl.df['price'].median():,.0f}", className="kpi-value text-dark"),
                                html.Small("King County Area Median", className="text-muted")
                            ]
                        )
                    ),
                    dbc.Col(
                        sm=6, md=3,
                        children=html.Div(
                            className="kpi-card",
                            children=[
                                html.P("Champion Model Accuracy", className="kpi-label"),
                                html.Div("90.98%", className="kpi-value text-success"),
                                html.Small("R² Score (Test Split)", className="text-muted")
                            ]
                        )
                    ),
                    dbc.Col(
                        sm=6, md=3,
                        children=html.Div(
                            className="kpi-card",
                            children=[
                                html.P("Prediction Latency", className="kpi-label"),
                                html.Div("< 5 ms", className="kpi-value text-info"),
                                html.Small("Instant XGBoost Inference", className="text-muted")
                            ]
                        )
                    ),
                ]
            )
        ]
    )

