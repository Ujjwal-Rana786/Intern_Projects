#scraping books.toscrape.com
#importing the libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd 
from flask import Flask, request, render_template
import yfinance as yf


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')
    

@app.route('/aboutCodroid')
def aboutCodroid():
    return render_template('aboutCodroid.html')

@app.route('/aboutMe')
def aboutMe():
    return render_template('aboutMe.html')

@app.route('/blogs')
def blogs():
    return render_template('blogs.html')

@app.route('/WebScraping')
def WebScraping():
    return render_template('WebScraping.html')

@app.route('/PowerBI')
def powerbi():
    return render_template('PowerBI.html')

@app.route('/AIML')
def aiml():
    return render_template('AIML.html')

@app.route('/dataScience')
def dataScience():
    return render_template('dataScience.html')



@app.route('/bookTOScrape')
def scrape_books():
    books = []
    url = "http://books.toscrape.com/"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all book containers
        book_containers = soup.find_all('article', class_='product_pod')
        
        # Loop through each book container
        for book in book_containers:
            # Extract book title
            title_element = book.find('h3').find('a')
            title = title_element.get('title') if title_element else 'No title'
            
            # Extract book price
            price_element = book.find('p', class_='price_color')
            price = price_element.text if price_element else 'No price'
            
            # Extract availability
            availability_element = book.find('p', class_='instock availability')
            availability = availability_element.text.strip() if availability_element else 'No availability info'
            
            # Extract rating (optional)
            rating_element = book.find('p', class_='star-rating')
            rating = rating_element.get('class')[1] if rating_element else 'No rating'

            books.append({
                'Title': title,
                'Price': price,
                # 'availability': availability,
                # 'rating': rating,
            })
            
    except requests.RequestException as e:
        print(f"Error scraping the page: {e}")
    
    scraped_data =pd.DataFrame(books, columns=["Title","Price"] )
    
    return render_template("bookToScrape.html", table=scraped_data.to_html(index=False, classes="table table-striped"))

@app.route('/gcambala') 
def scrape_data():
    url = 'http://gcambalacantthry.edu.in/Faculty'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Successfully fetched the page!")
    else:
        print(f"Failed to retrieve the page! Status Code: {response.status_code}")
        return "Failed to fetch page", 500

    soup = BeautifulSoup(response.content, 'html.parser')

    faculty_info = []

    faculty_data = soup.find_all('div', {'class': 'contact-box'})

    for data in faculty_data:
        name_span = data.find('span', class_='text-primary')
        dept_span = data.find('span', id=lambda x: x and 'lblSubject' in x)
        post_span = data.find('span', id=lambda x: x and 'lblDesignation' in x)
        img_tag = data.find('img')

        fname = name_span.get_text(strip=True) if name_span else "N/A"
        fdept = dept_span.get_text(strip=True) if dept_span else "N/A"
        fpost = post_span.get_text(strip=True) if post_span else "N/A"
        fimg = img_tag['src'] if img_tag else ""

        faculty_info.append({
            'faculty_name': fname,
            'faculty_post': fpost,
            'faculty_dept': fdept,
            'faculty_photo': fimg
        })

    pd.set_option('display.max_rows', None)
   

    scraped_data = pd.DataFrame(faculty_info, columns=["faculty_name", "faculty_post", "faculty_dept", "faculty_photo"])

    return render_template("gcambala.html", table=scraped_data.to_html(index=False, classes="table table-striped"))


@app.route('/flipkart') 
def flipkart_data():
    url = "https://www.flipkart.com/search?q=laptop&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off"

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
 }

    response =requests.get(url, headers=headers) 
    response.raise_for_status()

    if response.status_code == 200:
       print(f"Successfully connected! Status Code: {response.status_code}")

       # Parse the HTML content of the page
       soup = BeautifulSoup(response.content, 'html.parser')
    

       # This list will store all the scraped data
       laptops = []

       # Find all containers for each product on the page.
       # This is a robust class name for the product cards on the Flipkart search page.
       product_containers = soup.find_all('div', class_='cPHDOP col-12-12')
    
       if not product_containers:
          print("No product containers found. The website structure may have changed. Please inspect the Flipkart page to find the new class names.")
       else:
          print(f"Found {len(product_containers)} products. Scraping data...")

          # Iterate through each product container to extract details
          for container in product_containers:
           try:
                 # Find the element containing the laptop name
                name_element = container.find('div', class_='KzDlHZ')
                name = name_element.get_text(strip=True) if name_element else 'N/A'

                # Find the element containing the price
                price_element = container.find('div', class_='yRaY8j ZYYwLA')
                price = price_element.get_text(strip=True) if price_element else 'N/A'

                # Find the element containing the rating
                rating_element = container.find('div', class_='XQDdHH')
                rating = rating_element.get_text(strip=True) if rating_element else 'N/A'

              
                exchange_offer_element = container.find('div', class_=['yiggsN', 'O5Fpg8'])

                    # Extract text or set to 'N/A' if element not found
                exchange_offer = exchange_offer_element.get_text(strip=True) if exchange_offer_element else 'N/A'


                # Add the extracted data to our list as a dictionary
                laptops.append({
                    'Laptop Name': name,
                    'Total Price': price,
                    'Exchange Offer': exchange_offer,
                    'Rating': rating,
                    #'Specifications': specifications
                })
           except Exception as e:
                # This will catch any errors with a specific product container 
                print(f"Error scraping the page: {e}")
                
           
          scraped_data = pd.DataFrame(laptops, columns=["Laptop Name","Total Price","Exchange Offer","Rating"]) 

          return render_template("flipkart.html", table=scraped_data.to_html(index=False, classes="table table-striped"))

       
    else:
      print(f"Failed to scrape the webpage. Status code: {response.status_code}")


@app.route('/BBCSports') 
def sports():
    url = "https://www.bbc.co.uk/sport/football/premier-league/table"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)

    print(f"Successfully connected! Status Code: {response.status_code}")

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all("table")
    league_table = tables[0] if tables else None

    teams_data = []

    if league_table:
      rows = league_table.find_all("tr")[1:]  # Skip header row
      for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 10:
            position = cols[0].get_text(strip=True)
            team_name = cols[1].get_text(strip=True)  # team name at index 1
            played = cols[2].get_text(strip=True)
            won = cols[3].get_text(strip=True)
            drawn = cols[4].get_text(strip=True)
            lost = cols[5].get_text(strip=True)
            goals_for = cols[6].get_text(strip=True)
            goals_against = cols[7].get_text(strip=True)
            goal_diff = cols[8].get_text(strip=True)


            teams_data.append({
                "Position": position,
                "Team": team_name,
                "Played": played,
                "Won": won,
                "Drawn": drawn,
                "Lost": lost,
                "Goals For": goals_for,
                "Goals Against": goals_against,
                "Goal Difference": goal_diff,
                
            })

  
    scraped_data = pd.DataFrame( teams_data , columns=["Position","Team","Played","Won","Drawn","Lost","Goals For","Golas Against","Goal Difference"])

    return render_template("BBCSports.html", table=scraped_data.to_html(index=False, classes="table table-striped"))

@app.route('/linkedin') 
def job():


   url = "https://www.linkedin.com/jobs/search?keywords=Software+Engineer&location=New+York"

   headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

   response = requests.get(url, headers=headers)

   soup = BeautifulSoup(response.content, "html.parser")

   jobs_list = []

   job_posts = soup.find_all("div", {"class": "base-card"})

   for job in job_posts:
      title = job.find("h3")
      company = job.find("h4")
      location = job.find("span", {"class": "job-search-card__location"})
    
      # Replace this with the actual class or tag of "Job Summary" if available
     
    
      job_data = []
      job_data.append(title.get_text(strip=True) if title else None)
      job_data.append(company.get_text(strip=True) if company else None)
      job_data.append(location.get_text(strip=True) if location else None)

    
      jobs_list.append(job_data)

   scraped_data = pd.DataFrame( jobs_list , columns=["title","company","location"])

   return render_template("linkedin.html", table=scraped_data.to_html(index=False, classes="table table-striped"))    




@app.route('/quote') 
def quote():
       
    all_quotes = []

    base_url = "https://quotes.toscrape.com"
    url = base_url

    while url:
      response = requests.get(url)
      soup = BeautifulSoup(response.text, 'html.parser')
    
      for quote_block in soup.find_all('div', class_='quote'):
        quote_text = quote_block.find('span', class_='text').get_text()
        author = quote_block.find('small', class_='author').get_text()
        tag_list = [tag.get_text() for tag in quote_block.find_all('a', class_='tag')]
        
        all_quotes.append({
            'Quote': quote_text,
            'Author': author,
            'Tags': ", ".join(tag_list)
        })
    
      next_button = soup.find('li', class_='next')
      if next_button:
        next_link = next_button.find('a')['href']
        url = base_url + next_link
      else:
        url = None


    scraped_data = pd.DataFrame( all_quotes , columns=["Quote","Author","Tags"])

    return render_template("quote.html", table=scraped_data.to_html(index=False, classes="table table-striped")) 


@app.route('/yahoofinance') 
def fetch_yahoo_finance_data():
    ticker_symbol = request.args.get('ticker', default='AAPL')  # Get ticker from the query string
    ticker = yf.Ticker(ticker_symbol)
    
    # Fetch 1 year historical data
    hist = ticker.history(period="1y").reset_index()  # reset_index for the date column
    
    # Prepare company info
    info = ticker.info
    company_data = {
    "Long Name": [info.get("longName", "N/A")],
    "Sector": [info.get("sector", "N/A")],
    "Industry": [info.get("industry", "N/A")],
    "Country": [info.get("country", "N/A")],
    "Website": [info.get("website", "N/A")],
}
    
    scraped_data = pd.DataFrame([company_data],  columns=["Long Name", "Sector", "Industry", "Country", "Website"])

    # Render two tables: company info and historical prices
    return render_template(
        "yahoofinance.html",
        company_table=scraped_data.to_html(index=False, classes="table table-striped"),
        history_table=hist.to_html(index=False, classes="table table-bordered")
    )


@app.route('/crpyto') 
def crpyto():
  
  crypto_ticker = "BTC-USD"
  btc = yf.Ticker(crypto_ticker)

  data = btc.history(start="2025-01-01", end="2025-09-01", interval="1d")
  
  return render_template(
        "crpyto.html",
        history_table=data.to_html(index=False, classes="table table-bordered")
    ) 


if __name__ == '__main__':
    app.run(debug=False, port=3000, host="0.0.0.0")