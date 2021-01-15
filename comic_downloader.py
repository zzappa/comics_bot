import requests
import re
import html
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
import random
import logging
import datetime

from links import smbc_latest
from utils import get_random_date, fetch_image


def get_xkcd(link):
    r = requests.get(link)
    logging.warning(r.url)
    try:
        urls_png = re.findall('https?://imgs.xkcd.com/.*png', r.text)
        urls_jpg = re.findall('https?://imgs.xkcd.com/.*jpe?g', r.text)
        url = urls_png[0] if urls_png else urls_jpg[0]
        i = fetch_image(url)
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
        url = urls_strips[0] if urls_strips else urls_images[0]
        i = fetch_image(url)
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
    i = fetch_image(img_url)
    txt = '\nSource: ' + r.url
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
    i = fetch_image(urls[0])
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
    i = fetch_image(urls[0])
    txt = '\nSource: ' + r.url
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
    src = '\nSource: ' + r.url
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
    try:
        txt = str(images[2]['alt']) + "\nSource: " + full_link
    except Exception:
        txt = None
    return i, txt


def get_phd(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html5lib')
    images = soup.findAll('img', {"id": "comic", "name": "comic"})
    url = images[0]["src"]
    i = fetch_image(url)
    try:
        txt = "\nSource: " + r.url
    except Exception:
        txt = None
    return i, txt
