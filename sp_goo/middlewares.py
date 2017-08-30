# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import logging
import time


from scrapy import signals
from fake_useragent import UserAgent
from selenium.common.exceptions import TimeoutException
from scrapy.http import HtmlResponse



logger = logging.getLogger(__name__)



class RandomUserAgentMiddleware(object):
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()

        self.ua = UserAgent()
        self.per_proxy = crawler.settings.get('RANDOM_UA_PER_PROXY', False)
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')
        self.proxy2ua = {}

    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)

        if self.per_proxy:
            proxy = request.meta.get('proxy')
            if proxy not in self.proxy2ua:
                self.proxy2ua[proxy] = get_ua()
                logger.debug('Assign User-Agent %s to Proxy %s' % (self.proxy2ua[proxy], proxy))
            request.headers.setdefault('User-Agent', self.proxy2ua[proxy])
        else:
            ua = get_ua()
            request.headers.setdefault('User-Agent', get_ua())


class JSPageMiddleware(object):

    def process_request(self, request, spider):
        if spider.name == "JobBole":
            try:
                spider.browser.get(request.url)
            except TimeoutException:
                print('30秒timeout之后，直接结束本页面')
                spider.browser.execute_script('window.stop()')

            time.sleep(3)

            print("访问：{0}".format(request.url))


            return HtmlResponse(url=spider.browser.current_url, 
                    body=spider.browser.page_source, encoding="utf-8",
                    request=request)




"""
class SpGooSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

"""
