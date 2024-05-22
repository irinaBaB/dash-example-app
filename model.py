import pandas as pd


"""modelling data to fit to the map and pie chart"""
data = pd.read_csv('melb_data.csv')

""""create dataset: suburb , rooms, price, date, Latitude, Longitude, Regionname"""
#create dataset: suburb , rooms, price, date, Latitude, Longitude, Regionname
selected_df = data[['Suburb','Rooms','Date','Lattitude','Longtitude','Regionname']]


""""Count number of suburbs for each Region"""
suburb_counts = selected_df.groupby(['Regionname', 'Suburb']).size().reset_index(name='Count')

"""Selecting top 10 Suburbs for each Region"""
def get_top_10_suburbs_per_region(df):
    top_suburbs = df.groupby('Regionname').apply(lambda x: x.nlargest(10,'Count')).reset_index(drop=True)
    return top_suburbs

top_10_suburbs = get_top_10_suburbs_per_region(suburb_counts)

"""Getting a Percentage of sale for each Subabrb in Region"""
final_top_10=pd.read_csv('top_10_suburbs.csv')
final_top_10['Pecent_Of_Sale'] = final_top_10["Pecent_Of_Sale"].round(2)


"""Total number of sales:"""
sales_by_region = selected_df['Regionname'].value_counts().reset_index()
