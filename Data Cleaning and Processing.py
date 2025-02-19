#Problem Statement : Learn how to collect data via web scraping, APIs, and data connectors from suitable sources as specified by the instructor. Also, remove the comments and provide the expected output.

import requests
import re
import sqlite3
import pandas as pd

# Web Scraping
url = "http://books.toscrape.com/"
response = requests.get(url)

if response.status_code == 200:
    print("Successfully connected to the website!")
    html = response.text

    title_pattern = re.compile(r'<h3>\s*<a href=".*?" title="(.*?)"')
    price_pattern = re.compile(r'<p class="price_color">(.*?)</p>')
    rating_pattern = re.compile(r'<p class="star-rating (.*?)">')
    
    titles = title_pattern.findall(html)
    prices = price_pattern.findall(html)
    ratings = rating_pattern.findall(html)
    
    books_data = [{'Title': title, 'Price': price, 'Rating': rating} 
                  for title, price, rating in zip(titles, prices, ratings)]
    
    with open('books_data.csv', 'w', encoding='utf-8') as file:
        file.write('Title,Price,Rating\n')
        for book in books_data:
            file.write(f'{book["Title"]},{book["Price"]},{book["Rating"]}\n')
    
    for i, book in enumerate(books_data[:5], 1):
        print(f"{i}. Title: {book['Title']}, Price: {book['Price']}, Rating: {book['Rating']}")
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)

# API Request
api_key = "YOUR_API_KEY"
city = "London"
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
response = requests.get(url)

if response.status_code == 200:
    print("Successfully fetched data from the API!")
    data = response.json()
    temperature = data['main']['temp']
    weather_description = data['weather'][0]['description']
    print(f"Weather in {city}: {weather_description}, Temperature: {temperature}C")
else:
    print("Failed to fetch data. Status code:", response.status_code)

# SQLite Database
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        price REAL NOT NULL,
        rating TEXT NOT NULL
    )
''')

cursor.execute("INSERT INTO books (title, price, rating) VALUES (?, ?, ?)",
               ('A Light in the Attic', 51.77, 'Three'))
cursor.execute("INSERT INTO books (title, price, rating) VALUES (?, ?, ?)",
               ('Tipping the Velvet', 53.74, 'One'))

conn.commit()
conn.close()
