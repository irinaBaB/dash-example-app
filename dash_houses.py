from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from model import selected_df, final_top_10,sales_by_region

import dash_bootstrap_components as dbc


app = Dash(__name__)

unique_regions = final_top_10['Regionname'].unique()

app.layout = html.Div(children=[
        #create dropdown for the page
    html.Div([
        dbc.Row([ html.Div(html.H2('Melbourne House Market 2016-2017'),
                       style={'textAlign': 'center', 'fontWeight': 'bold', 'family': 'georgia'}) ]),
        html.Div(
                [
                    #html.H4("Analysis of sales by Suburbs"),
                    dcc.Dropdown(
                        id="region-dropdown",
                        options=[{"label": region, "value": region} for region in unique_regions],
                        value="Western Metropolitan",
                        style={"width": "300px"},
                        clearable=False,
                    ),
                ],
                style={"display": "flex", "flexDirection": "column", "alignItems": "flex-start", "marginBottom": "20px"}),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Row([
        dbc.CardBody(
            [
                dcc.Markdown(
                id="markdown-value",
                children=[])

            ]

        )
    ]),
        html.Br(),
        html.Br(),
        dbc.Row([  html.Div([
        html.Div([
            dcc.Graph(id="pie-chart")
        ], style={"flex": "1", "padding": "40px"}),

        html.Div([
            dcc.Graph(id="map-chart")
        ], style={"flex": "1", "padding": "40px"})
    ], style={"display": "flex", "width": "100%", "justifyContent": "space-between", "alignItems": "center"})])
      
    ])
])


@app.callback(
    Output(component_id="pie-chart", component_property="figure"),
    Input(component_id="region-dropdown", component_property="value"))


def generate_pie_chart(selected_region):
    filtered_df = final_top_10[final_top_10['Regionname'] == selected_region]
    fig = px.pie(filtered_df, names='Suburb',values ='Pecent_Of_Sale', title=f"Percentage of Sale of Suburb in {selected_region}", hole=0.4)
    fig.update_layout(
        height=578,  # Adjust height in pixels
        width=1000,   # Adjust width in pixels
        margin=dict(l=40, r=40, t=40, b=40)  # Adjust margins
    )
    return fig

@app.callback(
    Output(component_id="map-chart", component_property="figure"),
    Input(component_id="region-dropdown", component_property="value")
)

def generate_map_chart(selected_region):
    filtered_df = selected_df[selected_df['Regionname'] == selected_region]
    fig = px.scatter_mapbox(
       filtered_df,
        lat="Lattitude",
        lon="Longtitude",
        hover_name="Suburb",
        hover_data={"Suburb": True, "Regionname": True, "Lattitude": False, "Longtitude": False},
        color="Regionname",  # Optional: color by Regionname or any other relevant field
        zoom=10,
        height=600
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox=dict(
            center=dict(lat=filtered_df['Lattitude'].mean(), lon=filtered_df['Longtitude'].mean()),
            zoom=10
        ),
        margin=dict(l=4, r=4, t=4, b=4)
    )

    return fig

@app.callback(
    Output(component_id="markdown-value", component_property="children"),
    Input(component_id="region-dropdown", component_property="value")
)

def total_number_of_sales(selected_region):
    filtered_df = sales_by_region[sales_by_region['Regionname'] == selected_region]
    total_count = filtered_df['count'].sum()
    return f"**Total Value of Sales in {selected_region}:** {total_count}"




if __name__ == "__main__":
    print("Starting the Dash app...")
    app.run_server(debug=True, port=8053)
