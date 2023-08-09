import uuid, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import driver_path


def init_browser():
    """Initialize a Chrome browser."""
    options = Options()
    options.add_argument('disable-gpu')
    options.add_argument('--log-level=3')
    driver = webdriver.Chrome(service=Service(executable_path=driver_path), options=options)
    return driver


def get_artist_page(driver, starting_letter, starting_page):
    """Opens the artist page based on the starting letter and page number."""
    url = 'https://www.artsy.net/artists/artists-starting-with-{}?page={}'.format(starting_letter, starting_page)
    driver.get(url)


def click_next_page(driver):
    """Clicks on the next button to navigate to the next page."""
    pagination = driver.find_element('css selector', '[aria-label="Pagination"]')
    next_button = pagination.find_elements('xpath', '*')[-1]
    if next_button.get_attribute('href'):
        next_button.click()
        # time.sleep(1)
        return True
    else:
        print('No more pages in current letter.')
        return False


def get_artist_data(driver, artist_id, artist_link):
    """Gets artist data, and returns artist details as a dictionary."""
    driver.get(artist_link)
    artist_block = driver.find_element('xpath', '//*[@id="main"]/div/div[2]/div/div[1]/div/div[2]')
    # //*[@id="main"]/div/div[2]/div/div[1]/div/div[2]
    if len(artist_block.find_elements('xpath', '*')) > 1:
        artist_name, artist_info = artist_block.text.split('\n')
    else:
        artist_name = artist_block.text
        artist_info = None

    if len(driver.find_elements('xpath', '//*[contains(text(), "no works for sale")]')) > 0:
        art_num = 0
    else:
        fresnel_blocks = driver.find_elements('class name', 'fresnel-container')
        for fresnel in fresnel_blocks:
            num_block = fresnel.find_elements('xpath', '//*[contains(text(), " Artwork:") or contains(text(), " Artworks:")]')
            if len(num_block) > 0:
                break
        art_num = int(num_block[0].text.split(' ')[0].replace(",", ""))
        # print('Number of artworks: {}'.format(art_num))

    artist_data = {
        'artist_id': artist_id,
        'artist_name': artist_name,
        'artist_info': artist_info,
        'artist_link': artist_link,
        'art_num': art_num
    }

    return artist_data


def get_art_data(driver, art_link, artist_name):
    """Gets artwork information, creates a unique artwork_id, and returns artwork details as a dictionary."""
    driver.get(art_link)
    art_guid = uuid.uuid4().hex
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="artworkSidebar"]')))
    artwork_sidebar = driver.find_element('css selector', '[data-test="artworkSidebar"]')
    art_name = artwork_sidebar.find_element('xpath', './h1/i').text
    art_loc = artwork_sidebar.find_element('xpath', './h1').text.split(', ')[-1]
    art_sale = artwork_sidebar.find_elements('css selector', '[data-test="SaleMessage"]')
    art_price = art_sale[0].text if len(art_sale) > 0 else ''
    # art_matierial = artwork_sidebar.find_element('xpath', './div[3]/div[1]').text
    # art_size = artwork_sidebar.find_element('xpath', './div[3]/div[2]').text

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="artworkDetails"]')))
    art_detail = driver.find_elements('css selector', '[class*="ReadMore__Container"]')
    if len(art_detail) > 0:
        art_detail[0].click()
        art_des = art_detail[0].text
    else:
        art_des = ''

    art_data = {
        'artwork_id': art_guid,
        'artwork_title': art_name,
        'artwork_author': artist_name,
        'artwork_locale': art_loc,
        'artwork_link': art_link,
        'artwork_price': art_price,
        'artwork_description': art_des,
        # 'artwork_material': art_material,
        # 'artwork_size': art_size
    }

    return art_data