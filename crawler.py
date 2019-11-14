# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import argparse
import json

from inscrawler import InsCrawler
from inscrawler.settings import override_settings
from inscrawler.settings import prepare_override_settings
import filter_posts

import pymongo
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['scc-hotplace']
collection = db['posts']

from collections import OrderedDict

def get_posts_by_hashtag(tag, number, debug):
    ins_crawler = InsCrawler(has_screen=debug)
    return ins_crawler.get_latest_posts_by_tag(tag, number)


def output(data, tag=""):
    out = json.dumps(data, ensure_ascii=False)

    out = filter_posts.start_filter(out, tag)
    
    # collection.drop()
    collection.insert_many(json.loads(out))

def sort_posts_per_area(area_name):
    db["areas"].delete_many({"area_name": area_name})

    temp_dict = {}
    posts = db["posts"].find({"area_name": area_name})
    print(posts.count())
    for doc in posts:
        venue_name = doc["venue_name"]
        if venue_name not in temp_dict:
            temp_dict[venue_name] = {"num_of_posts": 1, "posts": [doc["_id"]]}
        else: 
            temp_dict[venue_name]["posts"].append(doc["_id"])
            temp_dict[venue_name]["num_of_posts"] += 1

    db["areas"].insert_one({"area_name":area_name, "venues": temp_dict})
    print("check reading")
    data = db["areas"].find_one({"area_name": "성수"})
    print(data)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Instagram Crawler")
    prepare_override_settings(parser)
    args = parser.parse_args()
    override_settings(args)

    # collection.drop()
    # output(
    #         get_posts_by_hashtag("서울숲맛집", 5, False), "서울숲맛집"
    # )
    # output(
    #         get_posts_by_hashtag("성수맛집", 5, False), "성수맛집"
    # )
    # output(
    #         get_posts_by_hashtag("성수맛집", 5, False), "성수맛집"
    # )
    sort_posts_per_area("성수")
