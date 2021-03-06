import datetime
import logging
import random
from io import BytesIO

import requests
from PIL import Image


def get_random_date(start_year: int, start_month: int, start_day: int, format: str = '') -> str:
    """
    Get random date from start_date and today.
    :param format: if date need to be in specific str format, ie .strftime("%y%m%d")
    :return: formatted_date: str representation of random_date
    """
    end_date = datetime.date.today()
    start_date = datetime.date(start_year, start_month, start_day)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    if format:
        formatted_date = random_date.strftime(format)
    else:
        formatted_date = str(random_date)
    return formatted_date


def fetch_image(link):
    try:
        img = requests.get(link)
        logging.warning(img.url)
        i = Image.open(BytesIO(img.content))
    except Exception:
        i = None
    return i
