#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import urllib2
from selenium import webdriver
import time
import hashlib
import os
from urlparse import urlparse
import threading


class GifFight(object):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--start-fullscreen")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument('headless')
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    instance = None

    def __init__(self):
        chromedriver_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'chromedriver')
        self.browser = webdriver.Chrome(chrome_options=self.chrome_options, executable_path=chromedriver_path)

    @staticmethod
    def get_instance():
        if not GifFight.instance:
            GifFight.instance = GifFight()
        return GifFight.instance

    def get_images(self, keyword):
        url = u'http://pic.sogou.com/pic/emo/searchList.jsp?statref=classify_form&keyword=%s' % keyword
        try:
            self.browser.get(url)
            # self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            imgs = self.browser.find_element_by_id('emoListDiv').find_elements_by_tag_name('img')
            imgs = [img.get_attribute('src') for img in imgs]
            self.browser.quit()
        except Exception as e:
            print(e)
            return {
                'err': str(e),
                'imgs': []
            }
        else:
            return {
                'err': '',
                'imgs': self.download_images(imgs)
            }

    @staticmethod
    def download_images(urls, check=False):
        img_folder = os.path.join(os.path.expanduser("~"), '.figure-fight-sogou')
        if not os.path.exists(img_folder):
            os.mkdir(img_folder)

        def image_path(img_url):
            return os.path.join(img_folder, GifFight.extract_img_name(img_url))

        def worker(img_url, file_path):
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as handle:
                    response = urllib2.urlopen(img_url)
                    handle.write(response.read())

        if not check:
            files = []
            # print(urls)
            for url in urls:
                files.append(
                    {
                        'path': image_path(url),
                        'url': url
                    }
                )
                threading.Thread(target=worker, args=(url, files[-1]['path'])).start()
            return files
        else:
            for item in urls:
                if not os.path.exists(item['path']):
                    threading.Thread(target=worker, args=(item['url'], item['path'])).start()

    @staticmethod
    def extract_img_name(url):
        try:
            a = urlparse(url)
            basename = os.path.basename(a.path)
            return basename if '.' in basename else '%s.gif' % basename
        except:
            return "%s.gif" % hashlib.sha256(url.encode()).hexdigest()


if __name__ == '__main__':
    start = time.time()
    urls = GifFight.get_instance().get_images(u'滚犊子')

    print(urls)
    print(time.time() - start)
