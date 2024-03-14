#import get to call a get request on the site
from requests import get
from bs4 import BeautifulSoup
from warnings import warn
import pandas as pd

def craigslistCrawl(max_price=100000, zipcode=97341, query="car", max_dist=30):
    craigslist_request = f'https://corvallis.craigslist.org/search/sss?hasPic=1&max_price={max_price}&postal={zipcode}&postedToday=1&query={query}&search_distance={max_dist}'

    response = get(craigslist_request)

    if response.status_code != 200:
        warn('Request: {}; Status code: {}'.format(craigslist_request, response.status_code))

    html_soup = BeautifulSoup(response.text, 'html.parser')
    posts = html_soup.find_all('li', class_='cl-static-search-result')

    post_titles = []
    post_locations = []
    post_prices = []
    post_links = []
    post_images = []


    for post in posts:
        if (post.find('div', class_='title') is not None and post.find('a')["href"] is not None):
            title = post.find('div', class_='title').text.translate({ord(i): None for i in '\n'}).strip()
            price = post.find('div', class_='price').text.translate({ord(i): None for i in '\n'}).strip()
            link = post.find('a')["href"]

            new_request = link
            item_response = get(new_request)
            soup = BeautifulSoup(item_response.text, 'html.parser')
            try:
                image = soup.find('img', title='1')['src']
            except:
                image = None
            print(image)


            try:
                location = post.find('div', class_='location').text.translate({ord(i): None for i in '\n'}).strip()
            except:
                location = None

            post_titles.append(title)
            post_locations.append(location)
            post_prices.append(price)
            post_links.append(link)
            post_images.append(image)

    query_postings = pd.DataFrame({'Title': post_titles,
                                   'Price': post_prices,
                                   'Location': post_locations,
                                   'link': post_links,
                                   'Image': post_images,})
    query_postings.drop_duplicates(subset='link')

    return query_postings





if __name__ == "__main__":
    craigslistCrawl()