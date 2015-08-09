# -*- coding:utf-8 -*-

import urllib2
import urlparse
import hashlib


def md5(input_str):
    m = hashlib.md5()
    m.update(input_str)
    return m.hexdigest()


def make_a_request(url, referer=None):
    """
    create a http request
    :param url:
    :param referer:
    :return: urllib2.Request
    """
    o = urlparse.urlparse(url)
    hdr = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': o.netloc,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.45 Safari/537.36'
    }
    if referer:
        hdr['Referer'] = referer
    return urllib2.Request(url, headers=hdr)


def get_source_size(url, retry_times=1, referer=None):
    for i in range(0, retry_times):
        try:
            return get_url_length(url, referer)
        except:
            print "can't get size of %s, try %d" % (url, i)
    raise Exception("can't get size of %s, retry %d" % (url, retry_times))


def get_url_length(url, referer=None):
    request = make_a_request(url, referer)
    request.get_method = lambda: 'HEAD'
    try:
        response = urllib2.urlopen(request)
        content_length = response.info().getheader('Content-Length')
        if content_length:
            return int(content_length)
    except urllib2.URLError as e:
        print e
    return -1


def readable_size(content_length):
    if content_length < 1024:
        return "%d b" % content_length
    kb = content_length / 1024.0
    if kb < 1000:
        return "%.3f Kb" % kb
    mb = kb / 1024.0

    if mb < 1000:
        return "%.3f Mb" % mb

    gb = mb / 1024.0
    if gb < 1000:
        return "%.3f Gb" % gb

    tb = gb / 1024.0
    return "%.3f Tb" % tb


def download_chunk(url, start, end, retry_times=1, referer=None):
    for i in range(0, retry_times):
        try:
            return download(url, start, end, referer)
        except:
            print "can't download %s(%d-%d), try %d" % (url, start, end, i + 1)
    raise Exception("can't download %s(%d-%d), retry %d" % (url, start, end,
                                                            retry_times))


def download(url, start, end, referer=None):
    request = make_a_request(url, referer)
    request.headers['Range'] = 'bytes=%s-%s' % (start, end)

    page = urllib2.urlopen(request)
    return page.read()
