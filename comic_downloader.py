import datetime
import html
import logging
import random
import re
from urllib.request import urlopen
from lxml import html as lxml_html

import feedparser
import requests
from bs4 import BeautifulSoup

from links import smbc_latest
from utils import get_random_date, fetch_image


def get_xkcd(link):
    r = requests.get(link)
    logging.warning(r.url)
    src = f'[Source]({r.url}).'
    try:
        soup = BeautifulSoup(r.text, 'html5lib')
        img_url = soup.find_all("img")
        text = img_url[2]['title']
        title = img_url[2]['alt']
        url = 'https:' + (img_url[2]['srcset'].split(' '))[0]
        i = fetch_image(url)
        txt = title + '\n' + text + '\n' + src
    except Exception:
        i = None
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
        url = urls_strips[0]
        i = fetch_image(url)
    except Exception:
        i = None
    src = f'[Source]({r.url}).'
    try:
        soup = BeautifulSoup(r.text, 'html5lib')
        txt = soup.find("div", {"id": "blog_text"})
        txt = html.unescape(str(txt).lstrip('<div id="blog_text"><p>\n<p>').rstrip('</p></div></p>\n'))
        txt = str(lxml_html.fromstring(txt).text_content())
        for item in ('r/>', 'align="center">', 'a href="', '" target="_blank"', 're>', 'm>', 'strong>', '/p>'):
            txt = txt.replace(item, ' ')
        txt = txt.replace('r/>', '') + "\n" + src
    except Exception:
        txt = src
    try:
        title = soup.find("h1", {"class": "storytitle"})
        title = title.text
    except Exception:
        title = ''
    text = title + '\n' + txt
    return i, text


def get_poorlydrawnlines(link):
    r = requests.get(link)
    logging.warning(r.url)
    try:
        if r.url.endswith('comic/'):
            soup = BeautifulSoup(r.text, 'html5lib')
            list_of_comics = []
            for link in soup.find_all('a'):
                if ('png' or 'jpg') in str(link.get('href')):
                    list_of_comics.append(link.get('href'))
            url = list_of_comics[0]
        else:
            urls = re.findall('https?://www.poorlydrawnlines.com/wp-content/uploads/.*j?p?n?g', r.text)
            url = urls[0].split()[0]
            if url.endswith('><img'):
                url = url.rstrip('><img')
    except Exception:
        return None, None
    i = fetch_image(url)
    txt = f' [Source]({r.url}).'
    return i, txt


def get_poorlydrawnlines_archive(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html5lib')
    list_of_comics = []
    for link in soup.find_all('a'):
        list_of_comics.append(link.get('href'))
    del list_of_comics[:15]
    url = random.choice(list_of_comics)
    i, txt = get_poorlydrawnlines(url)
    return i, txt


def get_smbc(link):
    r = requests.get(link)
    urls = re.findall('https?://www.smbc-comics.com/comics/.*p?n?gi?f?', r.text)
    logging.warning(r.url)
    src = f' [Source]({r.url}).'
    try:
        txt = re.findall('img\stitle=.*id="cc-comic"', r.text)
        txt = txt[0].lstrip('img title="').split('"')[0]
        txt = html.unescape(txt) + src
    except Exception:
        txt = src
    if not urls:
        logging.warning(link)
        return None, None
    i = fetch_image(urls[0])
    return i, txt


def get_smbc_from_archive(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html5lib')
    list_of_comics = []
    for link in soup.find_all('option'):
        list_of_comics.append(link)
    del list_of_comics[0]
    rand = random.choice(list_of_comics)
    rand_clean = re.findall('comic.*"', str(rand))[0].rstrip('"')
    new_link = smbc_latest + rand_clean
    img, txt = get_smbc(new_link)
    return img, txt


def get_exo(link):
    r = requests.get(link)
    logging.warning(r.url)
    urls = re.findall('https?://www.exocomics.com/wp-content/uploads/.*jpg', r.text)
    i = fetch_image(urls[0])
    txt = f' [Source]({r.url}).'
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
    urls = re.findall('https?://64.media.tumblr.com/.*jpg', str(images[0]))
    src = f' [Source]({r.url}).'
    i = fetch_image(urls[0])
    try:
        txt = str(images[0]).split("src")[0].lstrip('<img alt=') + src
    except Exception:
        txt = src
    return i, txt


def get_dilbert(link, latest=False):
    if latest:
        date = str(datetime.date.today())
    else:
        date = get_random_date(1989, 4, 16)
    full_link = link + date
    r = requests.get(full_link)
    soup = BeautifulSoup(r.text, 'html5lib')
    images = soup.findAll('img')
    url = str(images[2]['src'])
    i = fetch_image(url)
    src = f' [Source]({full_link}).'
    try:
        txt = str(images[2]['alt']) + src
    except Exception:
        txt = None
    return i, txt


def get_phd(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html5lib')
    images = soup.findAll('img', {"id": "comic", "name": "comic"})
    url = images[0]["src"]
    i = fetch_image(url)
    txt = f' [Source]({r.url}).'
    return i, txt


def get_phd_random(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html5lib')
    list_of_comics = []
    for link in soup.find_all('a'):
        if 'http://www.phdcomics.com/comics/archive.php?comicid=' in str(link.get('href')):
            list_of_comics.append(link.get('href'))
    rand = random.choice(list_of_comics)
    i, txt = get_phd(rand)
    return i, txt


def get_new_yorker_cartoon(link):
    r = urlopen(link)
    page = BeautifulSoup(r, "html5lib")
    logging.warning(r.url)
    links = []
    for link in page.findAll("picture", {"class": "responsive-cartoon__image responsive-image"}):
        links.append(link)
    res = []
    for item in links:
        caption = re.findall('<img alt=.*" class="responsive-image__image', str(item))[0].\
            lstrip('<img alt="').\
            rstrip(' class="responsive-image__image')
        url = re.findall('class="responsive-image__image" sizes="100vw".* srcset=', str(item))[0].\
            lstrip('class="responsive-image__image" sizes="100vw" src="').\
            rstrip('" srcset=')
        logging.warning(url)
        i = fetch_image(url)
        txt = html.unescape(caption)
        res.append((i, txt))
    return [item for item in res[:2]]


def get_new_yorker_rss(link):
    rss_feed = feedparser.parse(link)
    logging.warning('checking rss')
    res = []
    for item in rss_feed.entries[:1]:
        url = item.link
        temp = get_new_yorker_cartoon(url)
        res.append(temp)
    return res


def get_pbf(link, latest=False):
    r = requests.get(link)
    src = f'\nSource: {r.url}.'
    page = BeautifulSoup(r.text, "html5lib")

    links = []
    for img in page.findAll("img", {"class": "lazyload"}):
        if 'https://pbfcomics.com/wp-content/uploads/' in str(img):
            links.append(img)
    try:
        if latest:
            title = links[4]['title']
            url = links[4]['data-src']
        else:
            title = links[3]['title']
            url = links[3]['data-src']
        logging.warning(url)
        img_url = f'Image: {url}'
        txt = title + '\n' + img_url + src
    except Exception:
        txt = None
    return None, txt


def get_from_gocomics(link):
    r = requests.get(link)
    logging.warning(r.url)
    page = BeautifulSoup(r.text, "html5lib")

    links = []
    for img in page.findAll("div", {'class': "comic__image js-comic-swipe-target"}):
        links.append(img)
    urls = re.findall('src="https://assets\.amuniversal\.com.*srcset', str(links[0]))
    url = urls[0].lstrip('src="').rstrip('" srcset"')
    logging.warning(url)
    i = fetch_image(url)
    txt = f"[Source.]({r.url})"
    return i, txt
