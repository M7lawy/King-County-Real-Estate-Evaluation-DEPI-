"""
layouts/ml_tab.py
Layout for Tab 3: Machine Learning Evaluation, Comparison Graphs, and Why XGBoost.
"""

from dash import dcc, html
import dash_bootstrap_components as dbc
import data_loader as dl

def get_ml_tab():
    """Builds the machine learning benchmarks and rationale tab."""
    return dbc.Container(
        fluid=True,
        children=[
            # TOP MODEL PERFORMANCE CARDS
            dbc.Row(
                className="g-3 mb-4",
                children=[
                    dbc.Col(
                        md=3,
                        children=html.Div(
                            className="kpi-card border-success border-2 shadow-sm",
                            children=[
                                html.Span("🏆 Champion Model", className="badge bg-success mb-2"),
                                html.H4("XGBoost Regressor", className="fw-bold mb-1"),
                                html.P("R² Score: 90.98%", className="text-success fw-bold fs-5 mb-0"),
                                html.Small("MAE: $64,599 | RMSE: $119,933", className="text-muted d-block")
                            ]
                        )
                    ),
                    dbc.Col(
                        md=3,
                        children=html.Div(
                            className="kpi-card shadow-sm",
                            children=[
                                html.Span("Benchmark 2nd", className="badge bg-primary mb-2"),
                                html.H4("Random Forest", className="fw-bold mb-1"),
                                html.P("R² Score: 88.98%", className="text-primary fw-bold fs-5 mb-0"),
                                html.Small("MAE: $72,425 | RMSE: $139,933", className="text-muted d-block")
                            ]
                        )
                    ),
                    dbc.Col(
                        md=3,
                        children=html.Div(
                            className="kpi-card shadow-sm",
                            children=[
                                html.Span("Benchmark 3rd", className="badge bg-warning text-dark mb-2"),
                                html.H4("Polynomial Ridge", className="fw-bold mb-1"),
                                html.P("R² Score: 83.21%", className="text-warning fw-bold fs-5 mb-0"),
                                html.Small("MAE: $92,827 | RMSE: $164,025", className="text-muted d-block")
                            ]
                        )
                    ),
                    dbc.Col(
                        md=3,
                        children=html.Div(
                            className="kpi-card shadow-sm",
                            children=[
                                html.Span("Baseline", className="badge bg-secondary mb-2"),
                                html.H4("Linear Regression", className="fw-bold mb-1"),
                                html.P("R² Score: 77.81%", className="text-danger fw-bold fs-5 mb-0"),
                                html.Small("MAE: $113,987 | RMSE: $255,705", className="text-muted d-block")
                            ]
                        )
                    ),
                ]
            ),

            # COMPARISON CHARTS ROW: R2 & MAE
            dbc.Row(
                className="g-4 mb-4",
                children=[
                    dbc.Col(
                        lg=6,
                        children=html.Div(
                            className="dashboard-card",
                            children=[
                                dcc.Graph(figure=dl.get_fig_ml_r2_comparison())
                            ]
                        )
                    ),
                    dbc.Col(
                        lg=6,
                        children=html.Div(
                            className="dashboard-card",
                            children=[
                                dcc.Graph(figure=dl.get_fig_ml_mae_comparison())
                            ]
                        )
                    ),
                ]
            ),

            # ACTUAL VS PREDICTED & RESIDUALS
            dbc.Row(
                className="g-4 mb-4",
                children=[
                    dbc.Col(
                        lg=6,
                        children=html.Div(
                            className="dashboard-card",
                            children=[
                                dcc.Graph(figure=dl.get_fig_ml_actual_vs_predicted())
                            ]
                        )
                    ),
                    dbc.Col(
                        lg=6,
                        children=html.Div(
                            className="dashboard-card",
                            children=[
                                dcc.Graph(figure=dl.get_fig_ml_residuals())
                            ]
                        )
                    ),
                ]
            ),

            # FEATURE IMPORTANCE CHART
            dbc.Row(
                className="g-4 mb-4",
                children=[
                    dbc.Col(
                        lg=12,
                        children=html.Div(
                            className="dashboard-card",
                            children=[
                                dcc.Graph(figure=dl.get_fig_ml_feature_importance())
                            ]
                        )
                    )
                ]
            ),

            # DEEP DIVE: WHY WE USED XGBOOST
            html.Div(
                className="dashboard-card",
                children=[
                    html.Div(
                        className="d-flex align-items-center gap-2 mb-3 pb-2 border-bottom",
                        children=[
                            html.I(className="bi bi-patch-check-fill text-success fs-3"),
                            html.H3("Why We Selected XGBoost as the Champion Model", className="mb-0 fw-bold")
                        ]
                    ),
                    html.P(
                        "During our experimental evaluation in MachineLearning.ipynb, we trained and rigorously benchmarked "
                        "four competing regression paradigms: Ordinary Linear Regression, Regularized Polynomial Ridge Regression (degree 2), "
                        "Random Forest Regressor (100 estimators), and Extreme Gradient Boosting (XGBoost Regressor). "
                        "XGBoost decisively outperformed all other models across every key metric. Below are the core technical justifications:",
                        className="text-muted"
                    ),

                    dbc.Row(
                        className="g-3 mt-2",
                        children=[
                            dbc.Col(
                                md=6,
                                children=html.Div(
                                    className="callout-xgboost h-100",
                                    children=[
                                        html.H5("1. Capturing Complex Non-Linear Interactions", className="fw-bold text-success"),
                                        html.P(
                                            "Real estate prices are deeply non-linear. The value of an extra 500 square feet depends radically on location (Medina vs. Auburn) "
                                            "and construction grade. While linear regression requires explicit polynomial crosses that explode feature dimensionality, "
                                            "XGBoost's decision tree ensembles naturally identify multi-way feature interactions (e.g., Waterfront × Grade × Living Area) "
                                            "without manual combinatorial engineering.",
                                            className="text-secondary small mb-0"
                                        )
                                    ]
                                )
                            ),
                            dbc.Col(
                                md=6,
                                children=html.Div(
                                    className="callout-xgboost h-100",
                                    children=[
                                        html.H5("2. Decisive Empirical Benchmark Dominance", className="fw-bold text-success"),
                                        html.P(
                                            "On King County's 4,323 test homes, XGBoost achieved an R² score of 0.9098 (explaining ~91% of price variance) and reduced the "
                                            "Mean Absolute Error to $64,599. Compared to Ordinary Linear Regression ($113,987 MAE), XGBoost saved over $49,300 in error per house, "
                                            "and surpassed Random Forest by >$7,800 MAE and 2.0% in R².",
                                            className="text-secondary small mb-0"
                                        )
                                    ]
                                )
                            ),
                            dbc.Col(
                                md=6,
                                children=html.Div(
                                    className="callout-xgboost h-100",
                                    children=[
                                        html.H5("3. Built-In Regularization & Overfitting Immunity", className="fw-bold text-success"),
                                        html.P(
                                            "Unlike standard Gradient Boosting Machines or deep neural nets, XGBoost formulates its objective function with native "
                                            "L1 (Lasso) and L2 (Ridge) penalties on tree leaf weights. Along with tree depth constraints (max_depth=6) and column subsampling (colsample_bytree=0.8), "
                                            "XGBoost effectively prevents overfitting even across King County's diverse micro-markets.",
                                            className="text-secondary small mb-0"
                                        )
                                    ]
                                )
                            ),
                            dbc.Col(
                                md=6,
                                children=html.Div(
                                    className="callout-xgboost h-100",
                                    children=[
                                        html.H5("4. Iterative Gradient Boosting Error Correction", className="fw-bold text-success"),
                                        html.P(
                                            "Random Forest builds independent trees and averages them (bagging). In contrast, XGBoost builds sequential trees where each new tree "
                                            "focuses specifically on the pseudo-residuals of previous trees. This iterative boosting mechanism excels at predicting rare luxury "
                                            "and edge-case properties that bagging and linear regressions consistently misprice.",
                                            className="text-secondary small mb-0"
                                        )
                                    ]
                                )
                            ),
                            dbc.Col(
                                md=6,
                                children=html.Div(
                                    className="callout-xgboost h-100",
                                    children=[
                                        html.H5("5. Handling Geospatial Spatial Non-Linearity", className="fw-bold text-success"),
                                        html.P(
                                            "Latitude and Longitude do not correlate linearly with price; prime housing borders irregular lakefronts and micro-neighborhoods. "
                                            "XGBoost's axis-aligned recursive splits partition latitude and longitude into high-value geographical bounding boxes, "
                                            "accounting for 16.0% of the model's total predictive power.",
                                            className="text-secondary small mb-0"
                                        )
                                    ]
                                )
                            ),
                            dbc.Col(
                                md=6,
                                children=html.Div(
                                    className="callout-xgboost h-100",
                                    children=[
                                        html.H5("6. Sub-Millisecond Production Inference Latency", className="fw-bold text-success"),
                                        html.P(
                                            "XGBoost's highly optimized C++ engine features cache-aware data structures and parallelized tree traversal. "
                                            "When users type feature inputs or click the map in this dashboard, the valuation is generated in less than 5 milliseconds, "
                                            "delivering a lightning-fast interactive web application experience.",
                                            className="text-secondary small mb-0"
                                        )
                                    ]
                                )
                            ),
                        ]
                    )
                ]
            )
        ]
    )

