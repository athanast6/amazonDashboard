import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np


data_filepath = "./dataset.csv"
# 2021 Amazon Product Sales Data
data = pd.read_csv(data_filepath)
data['n_reviews'] = data['n_reviews'].str.replace(',', '')
data['n_reviews'] = data['n_reviews'].str.replace('No customer reviews yet', '0').astype(float)
#data['price'] = data['price'].replace('Not available', float(0)).str.replace('$', '')
#data['price'] = data['price'].str.replace(',', '').astype(float)



# Define months for dropdown options
months = ['2021-02-01', '2021-03-01', '2021-04-01', '2021-05-01', '2021-06-01','2021-07-01']

#
names = data['name'].unique()

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([ #style={'margin': '0', 'padding': '0','backgroundColor': '#111111','height': '100vh'}'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 
    html.H1(children='Amazon Sales Dashboard', style={'textAlign': 'center','color':'#00A8E1'}),
    html.Div([
        html.Div([
        
        
            html.P(['Choose a product.'], style={'textAlign': 'left','color':'#00A8E1'}),
            dcc.Dropdown(
                id='product-name',
                options=[{'label': name, 'value': name} for name in names],
                
                style={'width': '750px', 'margin-bottom': '20px', 'justify-content': 'center','padding':5}
            ),

            dcc.Graph(
                id='reviews-by-product',
                
            ),
        ]),
    ]),

    html.Div([
        html.Div([

            html.P(['Choose a month to see popular products.'], style={'textAlign': 'left','color':'#00A8E1'}),
            dcc.Dropdown(
            id='month-dropdown',
            options=[{'label': month, 'value': month} for month in months],
            value='January',  # Default value
            style={'width': '500px', 'margin-bottom': '20px','padding':5}
            ),

            dcc.Graph(
                id='sales-chart',
                
            ),
        ]),
    ]),
], style={'textAlign': 'center', 'backgroundColor': '#111111','margin':-10,'padding':3})




# Define callback to update the chart based on selected month
@app.callback(
    Output('sales-chart', 'figure'),
    [Input('month-dropdown', 'value')]
)
def update_chart_1(selected_month):
    filtered_df = data.copy()
    # You can filter the dataframe based on the selected month here
    # For demonstration, I'll just filter based on the length of the selected month string

    filtered_df = filtered_df[filtered_df['date'] == selected_month]

    filtered_df['price'] = filtered_df['price'].replace('Not available', float(0)).str.replace('$', '').astype(float)


    filtered_df = filtered_df.sort_values(by='n_reviews', ascending=True)


    figure=px.bar(filtered_df, x='number', y='n_reviews',
            color='price',
            hover_data=['name', 'price'],
            title='Product Reviews At Month').update_layout(
            height=700,
            template='plotly_dark',
            xaxis_title='Product',    # Update x-axis label
            yaxis_title='Number of Reviews')

    return figure




# Define callback to update the chart based on selected month
@app.callback(
    Output('reviews-by-product', 'figure'),
    [Input('product-name', 'value')],
)
def update_chart_2(selected_product):
    filtered_df = data.copy()
    filtered_df = pd.DataFrame(filtered_df.sort_values(by='name'))
    

    #selected_product = np.where(names == selected_product)[0][0]
    filtered_df = filtered_df[filtered_df['name'] == selected_product]

    filtered_df['date'] = pd.to_datetime(filtered_df['date'])
    filtered_df['n_reviews'] 

    figure = px.scatter(filtered_df, x='date', y='n_reviews',
            color='price',
            hover_data=['name', 'price'],
            title='Product Reviews By Date').update_layout(
            height=700,
            template='plotly_dark',
            xaxis_title='Date',    # Update x-axis label
            yaxis_title='Number of Reviews')

    return figure


#update_chart_1(months[0])

#update_chart_2(selected_product_index)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
