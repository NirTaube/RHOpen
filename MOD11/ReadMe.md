# MARS WEATHER DATA 

This code is designed to scrape the latest news articles from the Mars news website. It utilizes Splinter and BeautifulSoup libraries to automate browsing and extract relevant text elements from the website.

### Deliverable 1 Scrape Titles and Preview Text from Mars News
#### Getting Started

To use this code, follow the instructions below:

Make sure you have the necessary dependencies installed, including Splinter and BeautifulSoup.
Set up the browser configuration. In this code, the Chrome browser is used, but you can modify it to use a different browser by changing the argument in the Browser() function.
Visit the Mars news website by providing the URL to the browser.visit() function. You can inspect the page using Chrome DevTools to identify the elements you want to scrape.
Scraping the Website

After visiting the website, the code creates a Beautiful Soup object and extracts all the text elements with the class "list_text". It then loops through these elements and prints the date, title, and preview text for each article.

To store the results, the code creates a list of dictionaries. Each dictionary represents a news article and contains two keys: 'Title' and 'Preview'. The title and preview text are extracted from the text elements and added to the dictionaries. Finally, the list of dictionaries is printed to confirm the successful extraction.

#### Usage and Further Analysis

The scraped news articles can be used for various purposes, such as creating a news feed, conducting sentiment analysis, or performing further analysis on the content. You can manipulate the data within the list of dictionaries to suit your specific requirements.

Once you have extracted the news articles, you can store them in a file, perform data analysis, or integrate them into a larger project.

Note: This code provides a basic framework for scraping Mars news articles. It assumes the structure of the website remains consistent. If any changes are made to the website's structure, you may need to update the code accordingly.



### Deliverable 2: Scrape and Analyze Mars Weather Data

This repository contains code for scraping and analyzing Mars weather data from a specific website. Below is an overview of the steps involved in the process.

### Steps:

Visit the Website: The code uses the Splinter library to automate browsing and visit the Mars Temperature Data Site. The URL used for scraping is provided in the code.
Scrape the Table: Beautiful Soup is used to create a Beautiful Soup object and scrape the data from the HTML table on the website.
Store the Data: The scraped data is assembled into a Pandas DataFrame, with columns corresponding to the table headings on the website.
Prepare Data for Analysis: The data types of certain columns are converted to appropriate types using Pandas methods like astype and to_datetime.
Analyze the Data: The dataset is analyzed using Pandas functions to answer specific questions, such as the number of months on Mars, the number of Martian days worth of data, the coldest and warmest months, and the months with the lowest and highest atmospheric pressure. Visualizations are created using Matplotlib to present the results.
Save the Data: The final DataFrame is exported to a CSV file for further use.
Requirements:

### The code requires the following libraries to be installed:

Splinter
BeautifulSoup
Matplotlib
Pandas

### Usage:

#### To run the code, follow these steps:

Make sure you have the required libraries installed.
Copy and paste the code into a Python environment or an IDE.
Execute the code step by step or all at once.
The analysis results will be displayed in the console, and the final DataFrame will be saved as a CSV file named mars_weather_data.csv.

## Key Findings
Key Findings:

Number of Months on Mars: The data collected indicates that there are 12 months on Mars. The number of data points varies for each month, with the highest count in the third month and the lowest count in the tenth month.
Martian Days of Data: The scraped dataset contains a total of 1867 Martian days' worth of data. This provides a substantial amount of data for analysis and insights into the Martian climate.
Coldest and Warmest Months on Mars: Based on the average minimum daily temperature, the third month is the coldest on Mars, while the eighth month is the warmest. It's important to note that even the warmest month on Mars is extremely cold by human standards.
Atmospheric Pressure on Mars: The sixth month exhibits the lowest average atmospheric pressure on Mars, while the ninth month has the highest average pressure. These findings shed light on the atmospheric conditions and variations on the planet.
Terrestrial Days in a Martian Year: Analyzing the daily minimum temperature suggests that a Martian year consists of approximately 675 Earth days. This aligns with the well-known fact that a Mars year is equivalent to 687 Earth days.
These findings provide valuable insights into the weather patterns and conditions on Mars. Further analysis and comparison with historical data could uncover additional insights, contributing to a deeper understanding of the Martian climate. Please note that these conclusions are based on the provided code and its assumptions. Actual weather conditions and patterns on Mars may vary and should be studied using more extensive and diverse datasets.