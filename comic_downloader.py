import requests
import re
import html
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
import random
import logging

from links import smbc_latest


def get_xkcd(link):
    r = requests.get(link)
    try:
        urls = re.findall('https://imgs.xkcd.com/.*png', r.text)
        img = requests.get(urls[0])
        i = Image.open(BytesIO(img.content))
    except Exception:
        i = None
        logging.warning(link)
    try:
        text = re.findall('{{Title.*}}', r.text)
        text = html.unescape(text[0].lstrip('{{Title text: ').rstrip('}}').lstrip('{{Title text: ').rstrip('}}'))
    except IndexError:
        text = ''
    return i, text


def get_goose(link):
    r = requests.get(link)
    clean_url = re.findall('url=https://abstrusegoose.com/.*"', r.text)
    url = clean_url[0].lstrip('url=').rstrip('"')
    r = requests.get(url)
    try:
        urls = re.findall('https?://abstrusegoose.com/strips/.*png', r.text.lower())
        urls2 = re.findall('https?://abstrusegoose.com/images/.*png', r.text.lower())
        img = requests.get(urls[0] or urls2[0])
        i = Image.open(BytesIO(img.content))
    except IndexError:
        i = None
        logging.warning(url)
    try:
        soup = BeautifulSoup(r.text, 'html5lib')
        txt = soup.find("div", {"id": "blog_text"})
        txt = html.unescape(str(txt).lstrip('<div id="blog_text"><p>\n<p>').rstrip('</p></div></p>\n'))
    except Exception:
        txt = ''
    return i, txt


def get_poorlydrawnlines(link, latest=False):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    list_of_comics = []
    for link in soup.find_all('a'):
        list_of_comics.append(link.get('href'))
    if latest:
        img_url = [i for i in list_of_comics if 'png' in i][0]
    else:
        del list_of_comics[:15]
        url = random.choice(list_of_comics)
        r = requests.get(url)
        urls = re.findall('http://www.poorlydrawnlines.com/wp-content/uploads/.*png', r.text)
        try:
            img_url = urls[0].split()[0]
        except Exception:
            logging.warning(url)
            return None, None
    try:
        img = requests.get(img_url)
        i = Image.open(BytesIO(img.content))
    except Exception:
        i = None
    return i, ''


def get_smbc(link, latest=False):
    r = requests.get(link)
    urls = re.findall('https://www.smbc-comics.com/comics/.*png', r.text)
    try:
        txt = re.findall('img\stitle=.*id="cc-comic"', r.text)
        txt = txt[0].lstrip('img title="').split('"')[0]
        txt = html.unescape(txt)
    except Exception:
        txt = ''
    if not urls:
        logging.warning(link)
        return None, None
    try:
        img = requests.get(urls[0])
        i = Image.open(BytesIO(img.content))
    except Exception:
        i = None
        logging.warning(urls[0])
    return i, txt


def get_smbc_from_archive(link, latest=False):
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
