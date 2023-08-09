import requests
from bs4 import BeautifulSoup

def scrape_books_info(url):
    # Send a GET request to the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return

    # Parse the content of the page with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the container that holds the book information
    author_containers = soup.find_all('div', class_='Box-sc-15se88d-0 ArtistsByLetter__Columns-sc-1f86lqh-0  jJWpXK')

    # Initialize a list to store book data
    author_data = []

    # Loop through each book container and extract the required information
    for container in author_containers:
        artwork_author = container.find('div', class_='Box-sc-15se88d-0 Text-sc-18gcpao-0  cgchZM').text.strip()
        # book_author = container.find('p', class_='book-author').text.strip()
        # book_price = container.find('span', class_='book-price').text.strip()

        # Store the extracted information in a dictionary
        author_info = {
            'author': artwork_author,
            # 'author': book_author,
            # 'price': book_price,
        }

        author_data.append(author_info)

    return author_data

if __name__ == "__main__":
    # Replace 'url_to_scrape' with the actual URL of the website you want to scrape
    url_to_scrape = 'https://www.artsy.net/artists/artists-starting-with-a'
    scraped_data = scrape_books_info(url_to_scrape)

    if scraped_data:
        # Display the scraped data
        for author in scraped_data:
            print(f"Title: {author['author']}")
            print("---")
    else:
        print("No data scraped. Check the URL or website structure.")
