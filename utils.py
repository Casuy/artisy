import csv
from pathlib import Path
import pandas as pd

from config import artists_path, output_artist_file, output_asset_file, output_relationship_file


def write_initial_csv_headers():
    """Writes the initial csv headers for the output files."""
    with open(output_artist_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['artist_id', 'artist_name', 'artist_info', 'art_num'])

    with open(output_asset_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['artwork_id', 'artwork_title','artwork_author','artwork_locale','artwork_link','artwork_price','artwork_description'])

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
