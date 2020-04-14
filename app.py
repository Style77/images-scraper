import os
import random
import re
import sys
import argparse
import time

import urllib
import urllib.request

from selenium import webdriver

from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options

PINTEREST_IMAGES_KEY = "hCL kVc L4E MIw"
# PINTEREST_VIDEOS_KEY = "hwa kVc MIw L4E"


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


parser = argparse.ArgumentParser(description='awesome')
parser.add_argument('url', type=str, help="Url to pinterest page that will get scrapped.")
parser.add_argument('--pinterest', type=str2bool, help="[wstaw tu jakies madre slowo] if page is Pinterest page.", default=False)  # todo
parser.add_argument('--images', type=str2bool, help=".", default=True)  # todo
# parser.add_argument('--videos', type=bool, help=".", default=False)  # todo
# parser.add_argument('--channel', type=int, help="Discord channel id.")  # todo
parser.add_argument('--geckopath', type=str, help="Geckdriver path.")  # todo

args = parser.parse_args()

URL_REGEX = r"^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"
if not re.match(URL_REGEX, args.url):
    raise ValueError("Url has to be in http/https format.")


cute_words = ["ambrosial", "appealing", "attractive", "captivating", "charming", "cute", "darling", "dear",
              "delectable", "delicious", "delightful", "dishy", "dreamy", "fetching", "heavenly", "hot", "luscious",
              "pleasing", "precious", "sexy", "suave"]


def random_name(*, cute=False):
    if cute:
        url = "https://random-word-api.herokuapp.com/word?number=3"
        r = requests.get(url)
        words = r.text.replace("[", "").replace("]", "").replace("\"", "")
        words = words.split(',')
    elif not cute:
        words = []
        while len(words) != 3:
            omg = random.choice(cute_words)
            if omg not in words:
                words.append(omg)
    else:
        raise Exception("no") # todo

    word = ""
    for word_ in words:
        word_ = list(word_)
        word_[0] = word_[0].upper()
        word_ = ''.join(word_)

        word += word_

    return word


base_dir = os.getcwd()


def download_image(url):
    if "236x" in url:
        url = url.replace("236x", "564x")

    f_name = random_name()
    f_name = f_name + ".png"

    print("[INFO] downloading {}".format(url))

    print(f_name)
    while os.path.exists(os.path.join(base_dir, f_name)):
        f_name = random_name()

    urllib.request.urlretrieve(url, os.path.join(base_dir, f_name))


def main():
    print(args)

    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Firefox(executable_path=args.geckopath or "{os.getcwd()}\utils\geckodriver.exe",
                               firefox_options=options)
    driver.get(args.url)
    if args.pinterest:  # so this is fucking broken for now todo
        script = "var imgs = document.getElementsByTagName('img'); var imgSrcs = []; for (var i = 0; i < imgs.length; i++) {if (imgs[i].className == '{IMAGES_KEY}') imgSrcs.push(imgs[i].src);} return imgSrcs;"
        script = script.replace("{IMAGES_KEY}", PINTEREST_IMAGES_KEY)
    else:
        script = "var imgs = document.getElementsByTagName('img'); var imgSrcs = []; for (var i = 0; i < imgs.length; i++) {imgSrcs.push(imgs[i].src);} return imgSrcs;"
    print(0)
    imgs = driver.execute_script(script)
    print(imgs)
    for img in imgs:
        print(img)
        download_image(img)


    # soup = BeautifulSoup(r.text, features="lxml")
    # imgs = soup.find_all("img")
    #
    # # print(imgs)
    # # print("\n".join(set(tag['src'] for tag in imgs)))
    # # if not imgs:
    # #     raise ValueError("Could not find any <img> tag on this page.")
    #
    # images = []
    # for img in imgs:
    #     images.append(img.get('src'))
    #     # if args.pinterest:
    #     #     if img['class'] == PINTEREST_IMAGES_KEY:
    #     #         print(1)
    # print(images)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f"everything done in {end-start}s")
