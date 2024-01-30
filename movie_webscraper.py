import requests
import os
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def fetch_movie_data(url):
    response = requests.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    title = soup.find(itemprop="name").get_text() if soup.find(itemprop="name") else "Not Available"
    rating = soup.find(class_="rating-box").b.get_text() if soup.find(class_="rating-box") else "Not Available"
    year = soup.find(class_="year").get_text() if soup.find(class_="year") else "Not Available"
    
    # run time does not have a unique name so I need to find it
    runtime_span = soup.find(class_="meta").find_all('span')
    runtime = "Not Available"
    for span in runtime_span:
        if "min" in span.get_text():
            runtime = span.get_text()
            break
    description = soup.find(class_="description").get_text() if soup.find(class_="description") else "Not Available"

    return {
        "Title": title,
        "Rating": rating,
        "Year": year,
        "Runtime": runtime,
        "Description": description
    }

# NEXT STEP IS TO CREATE A BROWSER EXTENSION TO UPDATE THE URL AUTOMATICALLY
url = ''
movie_data = fetch_movie_data(url)

# Get the date and time the movie was imported into the excel file (date/time watched)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
movie_data['Date Watched'] = current_time

# test
print(movie_data)

# excel file
excel_filename = "movie_data.xlsx"
if os.path.exists(excel_filename):
    # read existing data
    df = pd.read_excel(excel_filename)
else:
    # create a new dataframe if the file is not created
    df = pd.DataFrame()

# Append new data to the file
'''
PANDAS NO LONGER SUPPORTS APPEND METHOD
'''
#df = df.append(movie_data, ignore_index=True)

# append new data using concat
new_row = pd.DataFrame([movie_data])
df = pd.concat([df, new_row], ignore_index=True)

# save to excel file
df.to_excel(excel_filename, index=False)

print(f"Data saved to {excel_filename}")


