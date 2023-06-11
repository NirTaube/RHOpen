# Eat Safe, Love

Welcome to Eat Safe, Love! This repository contains code for analyzing food establishment data in the UK. Whether you're a food enthusiast, a researcher, or just curious about food hygiene scores, this code will help you explore and uncover interesting insights. So grab your favorite snack and let's get started!

Notebook Set Up

Before we dive into the analysis, let's set up our environment. We'll be using Python and some popular libraries for data manipulation and visualization. Make sure you have the following dependencies installed:

pymongo - Python driver for MongoDB
pprint - Pretty-printer for displaying MongoDB documents
pandas - Data manipulation library
python

```Python
# Import dependencies
from pymongo import MongoClient
from pprint import pprint
import pandas as pd

# Create an instance of MongoClient
mongo = MongoClient(port=27017)

# Assign the uk_food database to a variable name
db = mongo['uk_food']

# Review the collections in our database
food_db = mongo['uk_food']

# Assign the collection to a variable
establishments = db['establishments']
```

## Exploratory Analysis

Now that our environment is set up, let's dive into some exploratory analysis of the food establishment data. We'll be answering a few questions along the way. Buckle up!

#### Question 1: Which establishments have a hygiene score equal to 20?

```python

# Find the establishments with a hygiene score of 20
query = {'scores.Hygiene': 20}

# Use count_documents to display the number of documents in the result
count = establishments.count_documents(query)
print(f"There are {count} establishments with a hygiene score of 20.")

# Display the first document in the results using pprint
pprint(establishments.find_one(query))

# Convert the result to a Pandas DataFrame
df = pd.DataFrame(establishments.find(query))

# Display the number of rows in the DataFrame
print(f"There are {len(df)} rows in this DataFrame.")

# Display the first 10 rows of the DataFrame
df.head(10)
```

#### Question 2: Which establishments in London have a RatingValue greater than or equal to 4?
```python

# Find the establishments with London as the Local Authority and a RatingValue greater than or equal to 4
query_2 = {
    'LocalAuthorityName': {'$regex': 'London'},
    'RatingValue': {'$gte': 4}
}

# Use count_documents to display the number of documents in the result
count_2 = establishments.count_documents(query_2)
print(f"There are {count_2} establishments in London that have a RatingValue greater than or equal to 4.")

# Display the first document in the results using pprint
pprint(establishments.find_one(query_2))

# Convert the result to a Pandas DataFrame
df2 = pd.DataFrame(establishments.find(query_2))

# Display the number of rows in the DataFrame
print(f"There are {len(df2)} rows in this DataFrame.")

# Display the first 10 rows of the DataFrame
df2.head(10)
```
Question 3: Top 5 Establishments with a RatingValue of 5
To find the top 5 establishments with a RatingValue of 5, sorted by the lowest hygiene score and nearest to our new restaurant "Penang Flavours," we'll follow these steps:

Retrieve the latitude and longitude of "Penang Flavours" using the geocode.latitude and geocode.longitude fields.
Define a search area around "Penang Flavours" using a latitude and longitude range.
Create a query to find establishments with a RatingValue of 5 within the defined search area.
Sort the results by the lowest hygiene score using the scores.Hygiene field.
Limit the results to the top 5 establishments.
Here's the code to achieve this:

```python

# Find lat & lon of "Penang Flavours"
pprint(establishments.find_one({'BusinessName': 'Penang Flavours'}, {'geocode.latitude', 'geocode.longitude'}))

# Define search area
degree_search = 0.01
latitude = 51.490142
longitude = 0.08384

# Create query
query3 = {
    'RatingValue': 5,
    'geocode.latitude': {'$lte': latitude + degree_search, '$gte': latitude - degree_search},
    'geocode.longitude': {'$lte': longitude + degree_search, '$gte': longitude - degree_search}
}

# Sort by hygiene score
sort = [('scores.Hygiene', 1)]

# Print the results
results = establishments.find(query3).sort(sort).limit(5)
for result in results:
    pprint(result)
 ```
    
This code will provide you with the details of the top 5 establishments with a RatingValue of 5, sorted by the lowest hygiene score and nearest to "Penang Flavours."

I guess its not Fish and Chips after all
</>
