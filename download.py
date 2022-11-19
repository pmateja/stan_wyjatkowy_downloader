#!/usr/bin/env python3

import os
import requests
from lxml import etree
from datetime import datetime


storage = os.path.join(os.path.dirname(os.path.realpath(__file__)), "episodes")


def get_feed():
    url = "https://feeds.libsyn.com/176861/rss"
    feed = requests.get(url)
    return etree.fromstring(feed.content)

def get_new_episode():
    feed = get_feed()
    return feed.xpath("//item")[0]

def get_file(item):
    return item.xpath("//enclosure")[0].get("url")

def get_date(item):
    pubDate = item.xpath("//pubDate")[0].text
    return datetime.strptime(pubDate, "%a, %d %b %Y %H:%M:%S +%f")
    # return datetime.strftime(d, "%Y-%m-%d")

def run():
    episode = get_new_episode()
    if get_date(episode).date() == datetime.today().date():
        print(get_date(episode), "New episode, downloading:",get_file(episode))
        name = datetime.strftime(get_date(episode), "%Y-%m-%d")
        name = os.path.join(storage, name+".mp3")
        with open(name, "wb") as w:
            resp = requests.get(get_file(episode))
            w.write(resp.content)
            print("Episode saved to:", name)
            
        

if __name__ == "__main__":
    run()
    