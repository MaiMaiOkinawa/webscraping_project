import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

'''
The information required is Average Rank, Film, and Year.
You are required to write a Python script webscraping_movies.py 
that extracts the information and saves it to a CSV file top_50_films.csv. 
You are also required to save the same information to a database Movies.db under the table name Top_50.
'''

url = "https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films"
db_name = 'Movies.db'
table_name = 'Top_50'
csv_path = '../webscraping_project/top_50_films.csv'
df = pd.DataFrame(columns=['Average Rank', 'Film', 'Year'])
count = 0

html_page = requests.get(url).textpytho2
data = BeautifulSoup(html_page, 'html.parser')

tables = data.find_all('tbody')
rows = tables[0].find_all('tr')

'''
iterate over the rows to find the required data. 
Use the code shown below to extract the information.
'''
# Iterate over the contents of the variable rows.
for row in rows:
    # Check for the loop counter to restrict to 50 entries.
    if count < 50:
        # Extract all the td data objects in the row and save them to col
        col = row.find_all('td')
        # Check if the length of col is 0, that is, if there is no data in a current row. 
        # This is important since, many timesm there are merged rows that are not apparent in the web page appearance.
        if len(col)!=0:
            #Create a dictionary data_dict with the keys same as the columns 
            # of the dataframe created for recording the output earlier and corresponding values from the first three headers of data.
            data_dict = {'Average Rank': int(col[0].contents[0]),
                         'Film': str(col[1].contents[0]),
                         'Year': int(col[2].contents[0])}
            # Convert the dictionary to a dataframe
            df1 = pd.DataFrame(data_dict, index=[0])
            # concatenate it with the existing one
            #This way, the data keeps getting appended to the dataframe with every iteration of the loop.
            df = pd.concat([df,df1], ignore_index = True)
            # Increment the loop counter.
            count+=1
    # Once the counter hits 50, stop iterating over rows and break the loop.
    else:
        break

print(df)

df.to_csv(csv_path)

'''
To store the required data in a database, you first need to initialize a connection to the database, 
save the dataframe as a table, and then close the connection. 
'''
conn = sqlite3.connect(db_name)
df.to_sql(table_name, conn, if_exists='replace', index=False)
conn.close()