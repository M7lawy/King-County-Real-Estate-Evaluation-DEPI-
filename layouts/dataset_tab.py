"""
layouts/dataset_tab.py
Layout for Tab 4: Dataset Explorer and Data Dictionary.
"""

from dash import html, dash_table
import dash_bootstrap_components as dbc
import data_loader as dl

def get_dataset_tab():
    """Builds the dataset preview and data dictionary tab."""
    cols_to_show = ['price', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'waterfront', 'view', 'condition', 'grade', 'zipcode', 'house_age', 'is_renovated']
    sample_table = dl.df[cols_to_show].head(15).to_dict('records')

    data_dictionary = [
        {"Feature": "price", "Type": "Numeric ($)", "Description": "Final sale price of the house in USD (Target variable for prediction)."},
        {"Feature": "bedrooms", "Type": "Integer", "Description": "Number of bedrooms in the property (ranging 1 to 11)."},
        {"Feature": "bathrooms", "Type": "Float", "Description": "Number of bathrooms (with 0.25 = toilet only, 0.5 = toilet + sink, 0.75 = shower, 1.0 = full bath)."},
        {"Feature": "sqft_living", "Type": "Integer (sq ft)", "Description": "Square footage of the interior living space."},
        {"Feature": "sqft_lot", "Type": "Integer (sq ft)", "Description": "Square footage of the land lot parcel."},
        {"Feature": "floors", "Type": "Float", "Description": "Total number of levels/floors in the house (1 to 3.5)."},
        {"Feature": "waterfront", "Type": "Binary (0/1)", "Description": "Flag indicating whether property overlooks a waterfront (0 = No, 1 = Yes)."},
        {"Feature": "view", "Type": "Integer (0-4)", "Description": "Index rating the quality of property's scenic view (0 = None, 4 = Spectacular)."},
        {"Feature": "condition", "Type": "Integer (1-5)", "Description": "Overall condition of the house structure (1 = Poor, 5 = Very Good)."},
        {"Feature": "grade", "Type": "Integer (1-13)", "Description": "King County building construction quality grade (7 = Average, 11-13 = Custom Luxury Mansions)."},
        {"Feature": "zipcode", "Type": "Categorical", "Description": "Postal 5-digit zipcode in King County, Washington."},
        {"Feature": "lat / long", "Type": "Float (Degrees)", "Description": "Geographic latitude and longitude coordinates."},
        {"Feature": "sqft_living15", "Type": "Integer (sq ft)", "Description": "Living area square footage of the 15 nearest neighboring properties."},
        {"Feature": "sqft_lot15", "Type": "Integer (sq ft)", "Description": "Lot area square footage of the 15 nearest neighboring properties."},
        {"Feature": "has_basement", "Type": "Binary (0/1)", "Description": "Engineered flag: 1 if sqft_basement > 0, else 0."},
        {"Feature": "house_age", "Type": "Integer (Years)", "Description": "Engineered: Sale year minus year the house was built."},
        {"Feature": "is_renovated", "Type": "Binary (0/1)", "Description": "Engineered: 1 if year renovated > 0, else 0."},
        {"Feature": "years_since_renovation", "Type": "Integer", "Description": "Engineered: Years since renovation, or house age if unrenovated."},
        {"Feature": "living_to_lot_ratio", "Type": "Float", "Description": "Engineered: Ratio of living area to total lot area (density metric)."}
    ]

    return dbc.Container(
        fluid=True,
        children=[
            html.Div(
                className="dashboard-card",
                children=[
                    html.H5("📁 King County Housing Dataset Summary", className="card-title-custom"),
                    html.P("The dataset contains 21,612 historical house sales in King County, WA (including Seattle, Bellevue, Redmond, Kirkland, and surrounding areas).", className="text-muted"),
                    
                    html.H6("Sample Data Records (First 15 Rows)", className="fw-bold mt-4 mb-2"),
                    dash_table.DataTable(
                        data=sample_table,
                        columns=[{"name": col, "id": col} for col in cols_to_show],
                        page_size=10,
                        style_table={'overflowX': 'auto'},
                        style_header={
                            'backgroundColor': '#f8fafc',
                            'fontWeight': 'bold',
                            'color': '#1e293b',
                            'borderBottom': '2px solid #cbd5e1'
                        },
                        style_cell={
                            'padding': '8px 12px',
                            'fontSize': '0.85rem',
                            'fontFamily': 'Inter, sans-serif'
                        }
                    ),

                    html.H6("Data Dictionary & Feature Specifications", className="fw-bold mt-4 mb-2"),
                    dash_table.DataTable(
                        data=data_dictionary,
                        columns=[
                            {"name": "Feature", "id": "Feature"},
                            {"name": "Data Type", "id": "Type"},
                            {"name": "Description & Context", "id": "Description"}
                        ],
                        page_size=20,
                        style_table={'overflowX': 'auto'},
                        style_header={
                            'backgroundColor': '#f8fafc',
                            'fontWeight': 'bold',
                            'color': '#1e293b'
                        },
                        style_cell={
                            'padding': '8px 12px',
                            'fontSize': '0.85rem',
                            'textAlign': 'left',
                            'fontFamily': 'Inter, sans-serif'
                        },
                        style_cell_conditional=[
                            {'if': {'column_id': 'Feature'}, 'fontWeight': 'bold', 'width': '180px'},
                            {'if': {'column_id': 'Type'}, 'width': '140px'}
                        ]
                    )
                ]
            )
        ]
    )

