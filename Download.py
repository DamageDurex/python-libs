# coding=utf-8
import hashlib

import urllib2

import urllib

import os

import time

import cookielib

from scrapy.utils.python import to_bytes


class Img(object):
    def download(self, img_url, game, title, headers, delay, cookie=None):
        filename = self.get_file_name(img_url, game, title)
        # 文件夹是否存在
        path = '../../images/%s/%s' % (game, title)
        if not os.path.isdir(path):
            os.makedirs(path)
        # 图片是否存在
        if os.path.isfile('../../images/%s' % filename):
            return filename
        # 设置cookie
        # cookie_jar = cookielib.CookieJar()
        # cookie_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
        # urllib2.install_opener(cookie_opener)
        # request = urllib2.Request(img_url, headers=headers)
        # response = urllib2.urlopen(request)
        # 下载延迟
        time.sleep(delay)
        urllib.urlretrieve(url=img_url, filename='../../images/' + filename)
        # 写入图片
        # with open('../../images/' + filename, 'wb') as f:
        #     f.write(response.read())
        #     f.close()
        return filename

    def get_file_name(self, img_url, game, title):
        image_guid = hashlib.sha1(to_bytes(img_url)).hexdigest()
        return '%s/%s/%s.jpg' % (game, title, image_guid)
