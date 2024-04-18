import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


data_filepath = "./dataset.csv"
# 2021 Amazon Product Sales Data
data = pd.read_csv(data_filepath)

##df['n_reviews'] = df['n_reviews'].str.replace(',', '')
#df['n_reviews'] = df['n_reviews'].str.replace('No customer reviews yet', '0').astype(float)
#df['price'] = df['price'].replace('Not available', float(0)).str.replace('$', '').astype(float)
#df = df.sort_values(by='n_reviews', ascending=True)



# Define months for dropdown options
months = ['2021-02-01', '2021-03-01', '2021-04-01', '2021-05-01', '2021-06-01','2021-07-01']

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div(style={'margin': '0', 'padding': '0','backgroundColor': '#111111','display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'height': '100vh'}, children=[
    html.Div(style={'text-align': 'center','width': '75%'}, children=[
        html.H1("Amazon Sales Dashboard",style={'color': '#EEEEEE'}),
        
        dcc.Dropdown(
            id='month-dropdown',
            options=[{'label': month, 'value': month} for month in months],
            value='January',  # Default value
            style={'width': '200px', 'margin-bottom': '20px'}
        ),

        dcc.Graph(
            id='sales-chart',
            
        )
    ])
])


# Define callback to update the chart based on selected month
@app.callback(
    Output('sales-chart', 'figure'),
    [Input('month-dropdown', 'value')]
)
def update_chart(selected_month):
    filtered_df = data.copy()
    # You can filter the dataframe based on the selected month here
    # For demonstration, I'll just filter based on the length of the selected month string

    filtered_df = filtered_df[filtered_df['date'] == selected_month]
    filtered_df['n_reviews'] = filtered_df['n_reviews'].str.replace(',', '')
    filtered_df['n_reviews'] = filtered_df['n_reviews'].str.replace('No customer reviews yet', '0').astype(float)

    filtered_df['price'] = filtered_df['price'].replace('Not available', float(0)).str.replace('$', '').astype(float)


    filtered_df = filtered_df.sort_values(by='n_reviews', ascending=True)


    figure=px.bar(filtered_df, x='number', y='n_reviews',
            color='price',
            hover_data=['name', 'price'],
            title='Product Reviews At Month').update_layout(
            height=700,
            template='plotly_dark',
            xaxis_title='Product Id',    # Update x-axis label
            yaxis_title='Number of Reviews')

    return figure

update_chart(months[0])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
