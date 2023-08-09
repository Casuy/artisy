import os
from crawler import *
from utils import *
from config import *


def crawl_artists():
    """Crawls artist names."""
    driver = init_browser()

    # Loop through specified pages
    for i in range(starting_page, stopping_page + 1):
        if i == starting_page:
            get_artist_page(driver, starting_letter, i)

        # Wait until the artist page is loaded
        WebDriverWait(driver, 10).until(lambda driver: len(driver.find_elements('xpath', '//*[@id="main"]/div/div[3]/*'))<2)

        # Get artist info
        artists_elements = driver.find_element('css selector', '[class*=ArtistsByLetter]').find_elements('xpath', '*')
        artists_data = pd.DataFrame(columns=['Guid', 'Name', 'Link']).set_index('Guid', inplace=True)
        for _, artist in enumerate(artists_elements):
            artist_guid = uuid.uuid4().hex
            link = artist.find_element('xpath', '*').get_attribute('href')
            name = artist.text
            artist_data = {
                'Guid': artist_guid,
                'Name': name,
                'Link': link
            }
            new_df = pd.DataFrame(artist_data, index=[0])
            new_df.set_index('Guid', inplace=True)
            artists_data = pd.concat([artists_data, new_df])

        letter = driver.find_element('css selector', '[aria-label="Breadcrumb"]').find_element('xpath', './preceding::*[1]').text.split(' ')[-1]
        page = driver.current_url.split('=')[-1] if '=' in driver.current_url else '1'

        if not os.path.exists(artists_path):
            os.makedirs(artists_path)
        if page == starting_page:
            artists_data.to_csv('artists/Artist-{}.csv'.format(letter), header=True, index=True)
        else:
            artists_data.to_csv('artists/Artist-{}.csv'.format(letter), mode='a', header=False, index=True)
        print('Artists list obtained with initial {} on page-{}'.format(letter, page))

        # Navigate to next page
        if i < stopping_page:
            click_next_page(driver)

    driver.quit()


def get_artist_and_art_data():
    """Obtains artist and art data."""
    artists_data = get_artists_data_from_files()
    driver = init_browser()

    # Get links of existing data from output files
    # existing_artists = get_existing_links(output_artist_file, k='artist_link')
    existing_art = get_existing_links(output_asset_file, k='artwork_link')

    # Loop through each artist
    for artist in artists_data:
        artist_id, artist_name, artist_link = artist
        # if is_crawled(artist_link, existing_artists):
        #     print("This author {} has been crawled.".format(artist_name))
        #     continue

        artist_data = get_artist_data(driver, artist_id, artist_link)

        # Append artist data to csv file
        with open(output_artist_file, 'a', newline='', encoding='utf-8') as f:
            fieldnames = artist_data.keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow(artist_data)

        if artist_data['art_num'] == 0:
            continue

        # Get artwork links
        art_items = driver.find_elements('css selector', '[data-test="artworkGridItem"]')
        art_links = [a.find_element('xpath', './a').get_attribute('href') for a in art_items]

        # Loop through and collect artwork data for each artist
        for link in art_links:
            if is_crawled(link, existing_art):
                print("The artwork at {} has been crawled.".format(link))
                continue

            art_data = get_art_data(driver, link, artist_data['artist_name'])

            # Append artwork data to csv files
            with open(output_asset_file, 'a', newline='', encoding='utf-8') as f:
                fieldnames = art_data.keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writerow(art_data)

            # Append relationship data to csv files
            with open(output_relationship_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([artist_data['artist_id'], art_data['artwork_id']])

    driver.quit()


def main():
    """Main function to run the program."""
    write_initial_csv_headers()
    # crawl_artists()
    get_artist_and_art_data()


if __name__ == '__main__':
    main()
