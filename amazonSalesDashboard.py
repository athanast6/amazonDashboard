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
data['price'] = data['price'].replace('Not available', float(0))
data['price'] = data['price'].str.replace('$', '', regex=True)
data['price'] = data['price'].str.replace(',', '', regex=True).astype(float)


# Define dropdown options
months = ['2021-02-01', '2021-03-01', '2021-04-01', '2021-05-01', '2021-06-01','2021-07-01']
names = data['name'].unique()

# Can we examine the Products with the best review gains from 02-01 to 06-01
product_reviews_02_01 = data[data['date'] == '2021-02-01']
product_reviews_06_01 = data[data['date'] == '2021-06-01']
product_reviews_gains = pd.merge(product_reviews_02_01, product_reviews_06_01, on='name', how='left').dropna()
product_reviews_gains['increase'] = product_reviews_gains['n_reviews_y'] - product_reviews_gains['n_reviews_x']
product_reviews_gains['pct_increase'] = (product_reviews_gains['n_reviews_y'] - product_reviews_gains['n_reviews_x'])/product_reviews_gains['n_reviews_y']






# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([ #style={'margin': '0', 'padding': '0','backgroundColor': '#111111','height': '100vh'}'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 
    html.H1(children='Amazon Sales Dashboard', style={'textAlign': 'center','color':'#00A8E1'}),
    html.Img(src='/assets/amazon-Logo-2.png',style={'width':'400px'}),
    html.Div([
        html.Div([
        
        
            html.P(['Choose a product to see reviews by date.'], style={'textAlign': 'left','color':'#FEFFFF'}),
            dcc.Dropdown(
                id='product-name',
                options=[{'label': name, 'value': name} for name in names],
                
                style={'width': '750px', 'margin-bottom': '20px', 'align-content': 'center','padding':5}
            ),

            dcc.Graph(
                id='reviews-by-product',
                style={'margin-bottom': '10px','padding':25},
            ),
        ]),
    ]),

    html.Div([
        html.Div([

            html.P(['Choose a month to see popular products.'], style={'textAlign': 'left','color':'#FEFFFF','padding':5}),
            dcc.Dropdown(
                id='month-dropdown',
                options=[{'label': month, 'value': month} for month in months],
                value='January',  # Default value
                style={'width': '500px', 'margin-bottom': '20px','padding':5, 'justify-content':'center'},
            ),

            dcc.Graph(
                id='sales-chart',
                style={'margin-bottom': '10px','padding':25},
            ),
            html.P(['The Echo Dot suddenly appears with 1.06 Million Reviews in April. Its possible that Amazon combined reviews for various colorways.'], style={'textAlign': 'center','color':'#FEFFFF'}),
            
        ]),
    ]),

    html.Div([
        html.Div([

            #html.P(['Percent Increase by Review over 4 months (Feb 1st- Jun 1st).'], style={'textAlign': 'center','color':'#FEFFFF','padding':5}),

            dcc.Graph(
                id='reviews-pct-increase',
                style={'color': '#111111','margin-bottom': '10px','padding':25},\

                
                figure=px.bar(product_reviews_gains, x='name', y='pct_increase',
                    hover_data=['increase', 'n_reviews_y'],
                    title='Percent increase of reviews by product over 4 months (Feb 1st- Jun 1st).').update_layout(
                    height=700,
                    template='plotly_dark',
                    xaxis_title='Product',    # Update x-axis label
                    yaxis_title='Number of Reviews')
                    ),
        ]),
    ]),

    html.Div([
        html.Div([

            #html.P(['Percent Increase by Review over 4 months (Feb 1st- Jun 1st).'], style={'textAlign': 'center','color':'#FEFFFF','padding':5}),

            dcc.Graph(
                id='reviews-pct-increase',
                style={'color': '#111111','margin-bottom': '10px','padding':25},\

                
                figure=px.histogram(product_reviews_02_01, x='price', 
                                    nbins=20,
                                    title='Number of products by price').update_layout(
                                    height=700,
                                    template='plotly_dark',
                                    xaxis_title='Price',    # Update x-axis label
                                    yaxis_title='Count')
            ),
        ]),
    ]),

    html.Div([
        html.Div([

            

            dcc.Graph(
                id='reviews-pct-increase-1',
                style={'color': '#111111','margin-bottom': '10px','padding':25},

                
                figure=px.pie(product_reviews_02_01[0:15],
                                values='n_reviews',
                                names='name',
                                title='Top 15 Products Total Share of Reviews on Feb 1st, 2021',
                                template='plotly_dark',)
            ),
            dcc.Graph(
                id='reviews-pct-increase-2',
                style={'color': '#111111','margin-bottom': '10px','padding':25},

                
                figure=px.pie(product_reviews_06_01[0:15],
                                values='n_reviews',
                                names='name',
                                title='Top 15 Products Total Share of Reviews on Jun 1st, 2021',
                                template='plotly_dark',)
            ),
            dcc.Graph(
                id='reviews-pct-increase-3',
                style={'color': '#111111','margin-bottom': '10px','padding':25},

                
                figure=px.pie(product_reviews_02_01[15:30],
                                values='n_reviews',
                                names='name',
                                title='Top 16-30 Products Total Share of Reviews on Feb 1st, 2021',
                                template='plotly_dark',)
            ),
            dcc.Graph(
                id='reviews-pct-increase-4',
                style={'color': '#111111','margin-bottom': '10px','padding':25},

                
                figure=px.pie(product_reviews_06_01[15:30],
                                values='n_reviews',
                                names='name',
                                title='Top 16-30 Products Total Share of Reviews on Jun 1st, 2021',
                                template='plotly_dark',)
            ),

            html.P(['A possible sleeper product to look into selling would be the Roku Ultra 2020. It had 4,780 reviews on Feb 1st, and increased to 10,459 on Jun 1st.'], style={'textAlign': 'center','color':'#FEFFFF','padding':5}),
        ]),
    ]),

    
], style={'textAlign': 'center', 'backgroundColor': '#111111','margin':-10,'padding':3,
          'background-image': 'url("/assets/background-image.jpg")',
           'background-repeat': 'repeat',
           'background-size': 'cover',
           })




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
