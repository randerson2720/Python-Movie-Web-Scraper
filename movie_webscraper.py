import requests
import os
import tkinter as tk
from tkinter import messagebox
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

# clear button
def clear():
    url_entry.delete(0, tk.END)

# submit button and save data
def submit():
    url = url_entry.get()
    if url:
        try:
            movie_data = fetch_movie_data(url)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            movie_data['Date Watched'] = current_time

            excel_filename = "movie_data.xlsx"
            if os.path.exists(excel_filename):
                df = pd.read_excel(excel_filename)
            else:
                df = pd.DataFrame()

            new_row = pd.DataFrame([movie_data])
            df = pd.concat([df, new_row], ignore_index=True)

            df.to_excel(excel_filename, index=False)
            messagebox.showinfo("Success", f"Data saved to {excel_filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Warning", "Please enter a URL")

# set up GUI
# main window
root = tk.Tk()
root.title("Movie Web Scraper!")

# frame for the textbox and buttons
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# url entry
url_entry = tk.Entry(frame, width=50)
url_entry.pack(side=tk.LEFT, padx=(0,10))

# submit button
submit_button = tk.Button(frame, text="Submit", command=submit)
submit_button.pack(side=tk.LEFT)

# clear button
clear_button = tk.Button(frame, text="Clear", command=clear)
clear_button.pack(side=tk.LEFT)

# start the gui
root.mainloop()













# NEXT STEP IS TO CREATE A BROWSER EXTENSION TO UPDATE THE URL AUTOMATICALLY
'''
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
#PANDAS NO LONGER SUPPORTS APPEND METHOD
'''
#df = df.append(movie_data, ignore_index=True)

# append new data using concat
new_row = pd.DataFrame([movie_data])
df = pd.concat([df, new_row], ignore_index=True)

# save to excel file
df.to_excel(excel_filename, index=False)

print(f"Data saved to {excel_filename}")

'''
