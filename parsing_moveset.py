import requests
from bs4 import BeautifulSoup
import random

def is_valid_url(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

def parsing(user):

    user = user.lower()
    url = f'https://pokemondb.net/pokedex/{user}'
    if is_valid_url(url):
        data = dict()
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            meta_tag = soup.find('meta', {'property': 'og:image'})

            # find image link
            image_link = meta_tag.get('content') if meta_tag else None

            # fiding all <a> tags with href attributes containing keyword "/move/"
            matching_links = soup.find_all('a', href=lambda value: value and '/move/' in value)

            # Extract and print the text content and power of all matching links
            for link in matching_links:
                move_name = link.text

                # Find the next <td> tag after the current link
                power_td = link.find_next('td', class_='cell-num')
                if power_td:
                    power = power_td.text.strip()
                    data[move_name] = power

            data = {key: int(value) for key, value in data.items() if value != '—'}
            random_moves = dict(random.sample(data.items(), 4))
            return random_moves, image_link, user
    else:
        return False, False, False
