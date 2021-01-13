import requests
import re
import html
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
import random
import logging
import datetime
from urllib.parse import urlparse

from links import smbc_latest


def get_xkcd(link):
    r = requests.get(link)
    logging.warning(r.url)
    try:
        urls_png = re.findall('https?://imgs.xkcd.com/.*png', r.text)
        urls_jpg = re.findall('https?://imgs.xkcd.com/.*jpe?g', r.text)
        img = requests.get(urls_png[0] if urls_png else urls_jpg[0])
        i = Image.open(BytesIO(img.content))
    except Exception:
        i = None
    src = '\nSource: ' + r.url
    try:
        txt = re.findall('{{Title.*}}', r.text)
        txt = html.unescape(txt[0].lstrip('{{Title text:').rstrip('}}').lstrip('{{Title text: ').rstrip('}}')) + src
    except Exception:
        txt = src
    return i, txt


def get_goose(link):
    r = requests.get(link)
    clean_url = re.findall('url=https?://abstrusegoose.com/.*"', r.text)
    url = clean_url[0].lstrip('url=').rstrip('"')
    r = requests.get(url)
    logging.warning(r.url)
    try:
        urls_strips = re.findall('https?://abstrusegoose.com/strips/.*png', r.text)
        urls_images = re.findall('https?://abstrusegoose.com/images/.*png', r.text)
        img = requests.get(urls_strips[0] if urls_strips else urls_images[0])
        i = Image.open(BytesIO(img.content))
    except Exception:
        i = None
    src = '\nSource: ' + r.url
    try:
        soup = BeautifulSoup(r.text, 'html5lib')
        txt = soup.find("div", {"id": "blog_text"})
        txt = html.unescape(str(txt).lstrip('<div id="blog_text"><p>\n<p>').rstrip('</p></div></p>\n')) + src
    except Exception:
        txt = src
    return i, txt


def get_poorlydrawnlines(link, latest=False):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    list_of_comics = []
    for link in soup.find_all('a'):
        list_of_comics.append(link.get('href'))
    if latest:
        img_url = [i for i in list_of_comics if ('png' or 'jpg') in i][0]
    else:
        del list_of_comics[:15]
        url = random.choice(list_of_comics)
        r = requests.get(url)
        logging.warning(r.url)
        urls = re.findall('https?://www.poorlydrawnlines.com/wp-content/uploads/.*png', r.text)
        try:
            img_url = urls[0].split()[0]
        except Exception:
            i = None
            txt = ''
    try:
        img = requests.get(img_url)
        i = Image.open(BytesIO(img.content))
        txt = '\nSource: ' + r.url
    except Exception:
        i = None
        txt = ''
    return i, txt


def get_smbc(link):
    r = requests.get(link)
    urls = re.findall('https?://www.smbc-comics.com/comics/.*p?n?gi?f?', r.text)
    logging.warning(r.url)
    src = '\nSource: ' + r.url
    try:
        txt = re.findall('img\stitle=.*id="cc-comic"', r.text)
        txt = txt[0].lstrip('img title="').split('"')[0]
        txt = html.unescape(txt) + src
    except Exception:
        txt = src
    if not urls:
        logging.warning(link)
        return None, None
    try:
        img = requests.get(urls[0])
        i = Image.open(BytesIO(img.content))
    except Exception:
        i = None

    return i, txt


def get_smbc_from_archive(link):
    all = requests.get(link)
    soup = BeautifulSoup(all.text, 'html5lib')
    list_of_comics = []
    for link in soup.find_all('option'):
        list_of_comics.append(link)
    del list_of_comics[0]
    rand = random.choice(list_of_comics)
    rand_clean = re.findall('comic\/.*"', str(rand))[0].rstrip('"')
    new_link = smbc_latest + rand_clean
    img, txt = get_smbc(new_link)
    return img, txt


def get_exo(link):
    r = requests.get(link)
    logging.warning(r.url)
    urls = re.findall('https?://www.exocomics.com/wp-content/uploads/.*jpg', r.text)
    try:
        img = requests.get(urls[0])
        i = Image.open(BytesIO(img.content))
        txt = '\nSource: ' + r.url
    except Exception:
        i = None
        txt = ''
    return i, txt


def get_exo_archive(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    list_of_comics = []
    for link in soup.find_all('a'):
        list_of_comics.append(link.get('href'))
    del list_of_comics[-34:]
    url = random.choice(list_of_comics)
    img, txt = get_exo(url)
    return img, txt


def get_tom_gauld(link):
    r = requests.get(link)
    logging.warning(r.url)
    soup = BeautifulSoup(r.text, 'html.parser')
    images = soup.findAll('img')
    url = re.findall('https?://64.media.tumblr.com/.*jpg', str(images[0]))
    src = '\nSource: ' + r.url
    try:
        img = requests.get(url[0])
        i = Image.open(BytesIO(img.content))
    except Exception:
        i = None
    try:
        txt = str(images[0]).split("src")[0].lstrip('<img alt=') + src
    except Exception:
        txt = src
    return i, txt


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
    txt = _apod_title(soup) + "\n" + _apod_explanation(soup) + '\nSource: ' + res + " \n" + link
    return None, txt


def get_apod_random(link):
    date = _apod_random_date()
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


def _apod_random_date():
    end_date = datetime.date.today()
    start_date = datetime.date(1995, 6, 16)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)

    rand_date = random_date.strftime("%y%m%d")
    return rand_date
