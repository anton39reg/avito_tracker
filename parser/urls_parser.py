import requests
from bs4 import BeautifulSoup
import sys


def parse(url):
    r = requests.get(url)

    # TODO: add check status

    soup = BeautifulSoup(r.text, 'html.parser')

    res = {'url': url}

    if soup.find('span', class_='item-closed-warning__content'):
        res['status'] = 'closed/unpublished'
    elif soup.find('div', class_='b-404'):
        res['status'] = 'deleted'
        return res
    elif not soup.find('span', class_='title-info-title-text'):
        res['status'] = 'sold'
        return res
    else:
        res['status'] = 'open'

    res['id'] = int(soup.find('div', class_='item-view-search-info-redesign').find('span').text.split()[1])

    res['title'] = soup.find('span', class_='title-info-title-text').text

    res['price'] = int(soup.find('span', class_='js-item-price').get('content'))

    res['description'] = soup.find('div', class_='item-description-text').text

    return res

#
# if __name__ == '__main__':
#     print(parse(sys.argv[1]))
