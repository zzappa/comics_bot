import logging
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from utils import get_random_date


def get_apod(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html5lib')
    img_tags = soup.find_all('img')
    video_tags = soup.find_all('iframe')

    urls = [img['src'] for img in img_tags]
    vids = [str(vid['src']) for vid in video_tags]

    try:
        if 'http' not in urls[0]:
            # sometimes an image source can be relative
            # if it is provide the base url which also happens
            # to be the site variable atm.
            hostname = urlparse(link).hostname
            scheme = urlparse(link).scheme
            urls[0] = '{}://{}/{}'.format(scheme, hostname, urls[0])
            res = urls[0]
    except Exception:
        res = vids[0]
    logging.warning(res)
    img_src = f' [Image]({res}).'
    src = f' [Source]({link}).'
    txt = _apod_title(soup) + "\n" + _apod_explanation(soup) + img_src + src
    return None, txt


def get_apod_random(link):
    date = get_random_date(1995, 6, 16, "%y%m%d")
    url = link + date + '.html'
    logging.warning(url)
    img, txt = get_apod(url)
    return img, txt


def _apod_explanation(soup):
    # source - https://github.com/nasa/apod-api/blob/master/apod/utility.py
    # Handler for later APOD entries
    txt = soup.find_all('p')[2].text
    txt = txt.replace('\n', ' ').replace('  ', ' ').split(' Tomorrow\'s picture')[0].strip(' ')
    if txt == '':
        # Handler for earlier APOD entries
        texts = [x.strip() for x in soup.text.split('\n')]
        try:
            begin_idx = texts.index('Explanation:') + 1
        except ValueError as e:
            # Rare case where "Explanation:" is not on its own line
            explanation_line = [x for x in texts if "Explanation:" in x]
            if len(explanation_line) == 1:
                begin_idx = texts.index(explanation_line[0])
                texts[begin_idx] = texts[begin_idx].strip()
            else:
                raise e
        idx = texts[begin_idx:].index('')
        txt = ' '.join(texts[begin_idx:begin_idx + idx])
    try:
        txt = (txt[:4000] + '...') if len(txt) > 4000 else txt
    except Exception:
        return ''
    return txt


def _apod_title(soup):
    # source - https://github.com/nasa/apod-api/blob/master/apod/utility.py
    try:
        # Handler for later APOD entries
        number_of_center_elements = len(soup.find_all('center'))
        if (number_of_center_elements == 2):
            center_selection = soup.find_all('center')[0]
            bold_selection = center_selection.find_all('b')[0]
            title = bold_selection.text.strip(' ')
        else:
            center_selection = soup.find_all('center')[1]
            bold_selection = center_selection.find_all('b')[0]
            title = bold_selection.text.strip(' ')
        return title
    except Exception:
        # Handler for early APOD entries
        text = soup.title.text.split(' - ')[-1]
        title = text.strip()
        return title
