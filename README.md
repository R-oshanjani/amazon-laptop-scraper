 Globussoft – Task 1 (Amazon Laptop Scraper)
This repository contains the solution for Task 1 from the assignment.  
The task is to scrape laptop product details from Amazon.in and save them into a CSV file.
 Description
The script sends an HTTP request to Amazon.in search results using `requests`, parses the HTML using `BeautifulSoup`, extracts product information, and stores the results into a CSV file. The CSV filename includes a timestamp.
The script extracts the following fields:
  -Image URL  
- Title  
- Rating  
- Price  
- Result Type (Ad / Organic)
Data is collected from the first 3 pages of the search results.
Technologies Used
- Python  
- requests  
- beautifulsoup4  
- pandas  
How to Run
1. Install dependencies:
`bash
pip install -r requirements.txt
2.Run the script:
python name of the python.py
3.After execution, a CSV file will be generated in the format:
amazon_laptops_YYYYMMDD_HHMMSS.csv

