--Data Cleaning--

DESCRIPTION
The project utilizes EPA’s Air Quality Survey data, which is publicly available on Google’s BigQuery platform. This program starts by querying the data for the desired timeframe of Jan 2010 to Dec 2020 for each pollutant. Once the data is retrieved and converted to a pandas dataframe, the data is grouped by the FIPS number, a five-digit federal code that identifies county, and aggregated by the mean monthly AQI. This process is repeated  for each pollutant dataset and the resulting data is concatenated into one final dataframe.

INSTALLATION
numpy
python
jupyter-console
google-cloud-bigquery
 

EXECUTION
Run program to collect from Google BigQuery and clean data. 

Start with authentication of BigQuery. Instructions:

1. Create a project on Google Cloud Platform
2. Set up authentication through creating a service account from the project
3. Generate a json key, save json file locally and copy path
4. Set an environment variable by running export GOOGLE_APPLICATION_CREDENTIALS="insert path here" in your terminal 
5. In terminal, type: pip install --upgrade 'google-cloud-bigquery[bqstorage,pandas]'
6. Launch jupyter notebook locally, make sure the notebook location is accessible to the json path

Further instructions on authentication process: https://cloud.google.com/bigquery/docs/visualize-jupyter


