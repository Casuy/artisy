# artisy Project

This project creates a web scraper that collects data on artists and their artworks from the [Artsy](https://www.artsy.net/) website. The program is built using Python and Selenium, which is used to navigate and interact with the website.

## File Structure

The project contains the following files:

- main.py: The main script to run the program
- utils.py: Utility functions for the project
- crawler.py: Functions to handle web scraping
- config.py: Configuration settings for the web scraper
- README.md: This documentation

## Usage

1. Install [Python](https://www.python.org/)
2. Install the required libraries:

```bash
pip install pandas selenium
```

3. Download the appropriate [ChromeDriver executable](https://sites.google.com/a/chromium.org/chromedriver/downloads) for your system and update the `driver_path` in the `config.py` file.
4. Update the `starting_letter`, `starting_page`, and `stopping_page` in the `config.py` file to set the range of pages to crawl.
5. Run the main script:

```bash
python main.py
```

## How it Works

The program currently includes the following steps:
1. Crawling artist names based on the specified starting letter and page range
2. Creating CSV files for storing artist data
3. Retrieving artist and art data
4. Writing crawled data to CSV files (artists, assets, and relationships)

## Output

The program generates three CSV files containing the following data:
- artisy_artist.csv: Contains information about artists
- artisy_asset.csv: Contains information about artworks
- artisy_relationship.csv: Contains relationships between artists and their artworks

## Implemented Features

The currently implemented features include:

1. Crawling artist names based on the specified starting letter and page range.
2. Handling pagination for artists pages, i.e. clicking the "Next" button when available.
3. Retrieving artist and art data, and writing crawled data to CSV files (artists, assets, and relationships).
4. Adapting to the responsive layout by using relative paths instead of absolute paths and picking appropriate attribute names.
5. Waiting for the page loading circle to disappear before continuing to scrape data.
6. Ensuring the artwork description is loaded before scraping its data.


## Not Implemented

The following features are not yet implemented:

1. Handling 'Next' button logic for artwork pages, similar to the artist pagination.
2. Handling sign-up popups that may appear when staying on the website for an extended period. Might be solved by logging in using a Google account.
3. Error handling and logging for unexpected issues during crawling.
4. Throttling and proxy support to prevent IP bans.
5. A user-friendly command-line interface for configuring settings.
6. Handling cases where the website is updated during the crawling process, e.g. artworks no longer being available for sale.


## Dependencies

The following libraries are required to run the program:
- pandas: Used for data manipulation and analysis
- selenium: Used for automating web browsers