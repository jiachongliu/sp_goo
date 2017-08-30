__author__ = 'jiachongliu'
__date__ = '2017/8/30 19:04'

from scrapy.cmdline import execute

import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(["scrapy", "crawl", "jobbole"])
