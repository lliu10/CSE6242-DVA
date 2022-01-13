import pandas as pd
import numpy as np
from datetime import datetime 
from google.cloud import bigquery



client = bigquery.Client()



# Helper functions
def change_date(df: object)-> object:
    df['month'] = pd.to_datetime(df['month'], format='%Y-%m-%d')
    df['month'] = df['month'].dt.strftime('%m-%Y')
    return df

def add_fips_code(df:object)->object: 
    df['state_code'] = df['state_code'].astype('str')
    df['county_code'] = df['county_code'].astype('str')

    df['state_code'] = df['state_code'].str.zfill(2)
    df['county_code'] = df['county_code'].str.zfill(3)

    df['fips_code'] = df['state_code'] + df['county_code']

    df['fips_code']= df['fips_code'].astype('int64')

    return df


pollutants = ['co','o3','no2','so2','pm25_frm']

date_query = """SELECT  state_code, county_code, parameter_code, 
                parameter_name, latitude, longitude, date_local,
                aqi, state_name, county_name, event_type
                FROM `bigquery-public-data.epa_historical_air_quality.pollutant_daily_summary`
                AS pollutant WHERE pollutant.date_local BETWEEN '2010-01-01' AND '2020-12-31'"""

pollutant_monthly_dict = {}
total_data = pd.DataFrame()

for p in pollutants:
    pollutant_monthly_dict[p] = []
    
    q = date_query.replace("pollutant", p)
    temp = client.query(q).to_dataframe()
    temp = temp.rename(columns={"date_local":"month"})
    temp = change_date(temp)
    temp = add_fips_code(temp)
    
    months = temp['month'].unique().tolist()
    for m in months:
        mdf = temp[temp.month == m]
        agg_df = mdf.groupby(['fips_code',
                              'state_name',
                              'county_name', 
                             'parameter_name', 
                             'parameter_code',  ]).agg({'aqi': 'mean'}).reset_index()
      
        agg_df = agg_df.rename(columns={'aqi':'avg_aqi'})
        agg_df['month'] = m      
        pollutant_monthly_dict[p].append(agg_df)
    
    pollutant_monthly_dict[p] = pd.concat(pollutant_monthly_dict[p])
    total_data = pd.concat([total_data, pollutant_monthly_dict[p]])
    

    
total_data.reset_index(drop=True, inplace=True)
print("Size of aggregated data:", total_data.shape[0], "rows and",total_data.shape[1], "columns")

# Uncomment to output a csv of the data into current directory.
# total_data.csv("pollutant_data.csv", index=False)



