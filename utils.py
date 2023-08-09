import csv
from pathlib import Path
import pandas as pd

from config import *


def write_initial_csv_headers():
    """Writes the initial csv headers for the output files."""
    if not Path(output_artist_file).exists():
        with open(output_artist_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['artist_id', 'artist_name', 'artist_info', 'artist_link', 'art_num'])

    if not Path(output_asset_file).exists():
        with open(output_asset_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['artwork_id', 'artwork_title', 'artwork_author', 'artwork_locale', 'artwork_link', 'artwork_price', 'artwork_description'])

    if not Path(output_relationship_file).exists():
        with open(output_relationship_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['artist_id', 'artwork_id'])


def get_artists_data_from_files():
    """Loads artist data from the csv files and returns a list of artist dicts."""
    artists_data = []
    for f in Path(artists_path).glob('*.csv'):
        df = pd.read_csv(f, header=None)
        artists_data.extend(df.values.tolist())
    return artists_data


def get_existing_links(output_file, k):
    """Gets the existing links from the output file."""
    existing_links = []
    with open(output_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            existing_links.append(row[k])
    return existing_links


def is_crawled(link, existing_links):
    """Checks if the data has been crawled."""
    return link in existing_links #and link != existing_links[-1]