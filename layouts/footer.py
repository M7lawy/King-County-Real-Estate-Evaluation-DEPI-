"""
layouts/footer.py
Footer component for the dashboard.
"""

from dash import html

def get_footer():
    """Returns the footer element."""
    return html.Footer(
        className="text-center py-4 text-muted small border-top bg-white mt-5",
        children=[
            html.P(
                "King County Real Estate Valuation & Analytics Hub | Built with Plotly Dash & XGBoost",
                className="mb-1 fw-semibold"
            ),
            html.P(
                "Data: King County Assessor & Housing Records (21,612 Properties) | Model: XGBoost Regressor (R² = 90.98%)",
                className="mb-0 text-secondary"
            )
        ]
    )

