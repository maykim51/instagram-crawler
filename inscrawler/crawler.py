from __future__ import unicode_literals

import glob
import json
import os
import re
import sys
import time
import traceback
from builtins import open
from time import sleep

from tqdm import tqdm

from . import secret
from .browser import Browser
from .exceptions import RetryException
from .fetch import fetch_caption
from .fetch import fetch_comments
from .fetch import fetch_datetime
from .fetch import fetch_imgs
from .fetch import fetch_likers
from .fetch import fetch_likes_plays
from .fetch import fetch_details
from .fetch import fetch_hashtags
from .utils import instagram_int
from .utils import randmized_sleep
from .utils import retry

from area_list import area_list

class Logging(object):
    PREFIX = "instagram-crawler"

    def __init__(self):
        try:
            timestamp = int(time.time())
            self.cleanup(timestamp)
            self.logger = open("/tmp/%s-%s.log" % (Logging.PREFIX, timestamp), "w")
            self.log_disable = False
        except Exception:
            self.log_disable = True

    def cleanup(self, timestamp):
        days = 86400 * 7 # 1 day = 86400 seconds
        days_ago_log = "/tmp/%s-%s.log" % (Logging.PREFIX, timestamp - days)
        for log in glob.glob("/tmp/instagram-crawler-*.log"):
            if log < days_ago_log:
                os.remove(log)

    def log(self, msg):
        if self.log_disable:
            return

        self.logger.write(msg + "\n")
        self.logger.flush()

    def __del__(self):
        if self.log_disable:
            return
        self.logger.close()


class InsCrawler(Logging):
    URL = "https://www.instagram.com"
    RETRY_LIMIT = 10

    def __init__(self, has_screen=False):
        super(InsCrawler, self).__init__()
        self.browser = Browser(has_screen)
        self.page_height = 0

    # def _dismiss_login_prompt(self):
    #     ele_login = self.browser.find_one(".Ls00D .Szr5J")
    #     if ele_login:
    #         ele_login.click()

    # def login(self):
    #     browser = self.browser
    #     url = "%s/accounts/login/" % (InsCrawler.URL)
    #     browser.get(url)
    #     u_input = browser.find_one('input[name="username"]')
    #     u_input.send_keys(secret.username)
    #     p_input = browser.find_one('input[name="password"]')
    #     p_input.send_keys(secret.password)

    #     login_btn = browser.find_one(".L3NKy")
    #     login_btn.click()

    #     @retry()
    #     def check_login():
    #         if browser.find_one('input[name="username"]'):
    #             raise RetryException()

    #     check_login()

    def get_latest_posts_by_tag(self, tag, num):
        url = "%s/explore/tags/%s/" % (InsCrawler.URL, tag)
        self.browser.get(url)
        return self._get_posts_full_for_tag(tag, num)


    def _get_posts_full_for_tag(self, tag, num):
        @retry()
        def check_next_post(cur_key):
            ele_a_datetime = browser.find_one(".eo2As .c-Yi7")

            # It takes time to load the post for some users with slow network
            if ele_a_datetime is None:
                raise RetryException()

            next_key = ele_a_datetime.get_attribute("href")
            if cur_key == next_key:
                raise RetryException()
        
        def retrieve_hashtags(dict_post):
            caption = dict_post["caption"]
            temp = ""
            for tag in list(caption.replace("#", " #").split()):
                if tag[0] == "#":
                    temp += tag[1:]+" "
            hashtags = temp.split()
            return hashtags

        browser = self.browser
        browser.implicitly_wait(3)
        browser.scroll_down()
        browser.scroll_down()
        ele_post = browser.find_one(".v1Nh3 a")
        ele_post.click()
        dict_posts = {}

        pbar = tqdm(total=num)
        pbar.set_description("fetching")
        cur_key = None

        # Fetching all posts
        for _ in range(num):
            dict_post = {}

            # Fetching post detail
            try:
                check_next_post(cur_key)

                # Fetching datetime and url as key
                ele_a_datetime = browser.find_one(".eo2As .c-Yi7")
                cur_key = ele_a_datetime.get_attribute("href")
                dict_post["key"] = cur_key
                fetch_datetime(browser, dict_post)
                fetch_imgs(browser, dict_post)

                ele_img = browser.find_one(".KL4Bh img", ele_post)
                if "food" not in ele_img.get_attribute("alt"):
                    continue

                fetch_caption(browser, dict_post)
                fetch_hashtags(browser, dict_post)

                dict_post["hashtags"] = retrieve_hashtags(dict_post)
                del dict_post["caption"]

            except RetryException:
                sys.stderr.write(
                    "\x1b[1;31m"
                    + "Failed to fetch the post: "
                    + cur_key or 'URL not fetched'
                    + "\x1b[0m"
                    + "\n"
                )
                break

            except Exception:
                sys.stderr.write(
                    "\x1b[1;31m"
                    + "Failed to fetch the post: "
                    + cur_key if isinstance(cur_key,str) else 'URL not fetched'
                    + "\x1b[0m"
                    + "\n"
                )
                traceback.print_exc()

            self.log(json.dumps(dict_post, ensure_ascii=False))
            dict_posts[browser.current_url] = dict_post

            

            pbar.update(1)
            left_arrow = browser.find_one(".HBoOv")
            if left_arrow:
                left_arrow.click()

        pbar.close()
        posts = list(dict_posts.values())
        if posts:
            posts.sort(key=lambda post: post["datetime"], reverse=True)
        return posts





    # def _get_posts(self, num):
    #     """
    #         To get posts, we have to click on the load more
    #         button and make the browser call post api.
    #     """
    #     TIMEOUT = 600
    #     browser = self.browser
    #     key_set = set()
    #     posts = []
    #     pre_post_num = 0
    #     wait_time = 1

    #     pbar = tqdm(total=num)

    #     def start_fetching(pre_post_num, wait_time):
    #         ele_posts = browser.find(".v1Nh3 a")
    #         for ele in ele_posts:
    #             key = ele.get_attribute("href")
    #             if key not in key_set:
    #                 dict_post = { "key": key }
    #                 ele_img = browser.find_one(".KL4Bh img", ele)
    #                 # dict_post["caption"] = ele_img.get_attribute("alt")
    #                 caption = ele_img.get_attribute("alt")
    #                 ## FIXIT :: multiple images
    #                 dict_post["img_url"] = ele_img.get_attribute("src")
    #                 dict_post["hashtags"] = []

    #                 fetch_details(browser, dict_post)
    #                 fetch_caption(browser, dict_post)

    #                 ## filter food-relevant only
    #                 if "food" in caption:
    #                     key_set.add(key)
    #                     posts.append(dict_post)
                    
    #                 # key_set.add(key)
    #                 # posts.append(dict_post)

    #                 if len(posts) == num:
    #                     break

    #         if pre_post_num == len(posts):
    #             pbar.set_description("Wait for %s sec" % (wait_time))
    #             sleep(wait_time)
    #             pbar.set_description("fetching")

    #             wait_time *= 2
    #             browser.scroll_up(300)
    #         else:
    #             wait_time = 1

    #         pre_post_num = len(posts)
    #         browser.scroll_down()

    #         return pre_post_num, wait_time

    #     pbar.set_description("fetching")
    #     while len(posts) < num and wait_time < TIMEOUT:
    #         post_num, wait_time = start_fetching(pre_post_num, wait_time)
    #         pbar.update(post_num - pre_post_num)
    #         pre_post_num = post_num

    #         loading = browser.find_one(".W1Bne")
    #         if not loading and wait_time > TIMEOUT / 2:
    #             break

    #     pbar.close()

    #     # add restaurant name


    #     print("Done. Fetched %s posts." % (min(len(posts), num)))
    #     return posts[9:num]
