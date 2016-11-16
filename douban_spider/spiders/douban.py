# -*- coding: utf-8 -*-

from douban_spider.items import DoubanSpiderItem
from scrapy.spidermiddlewares.httperror import *
import scrapy
import pybloomfilter
import user_settings
import json
import os

class DoubanSpider(scrapy.Spider):
	name = 'douban_spider'

	def __init__(self):
		self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0',}
		if os.path.exists('douban_spider.bloom'):
			self.blfilter = pybloomfilter.BloomFilter.open('douban_spider.bloom')
		else:
			self.blfilter = pybloomfilter.BloomFilter(user_settings.FILTER_SIZE,user_settings.FILTER_ERROR_RATE,'douban_spider.bloom')

	def start_requests(self):
		start_url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0'
		yield scrapy.Request(url=start_url,callback=self.parse_list,headers=self.headers,errback=self.parse_error)

	def parse_error(self,failure):
		if isinstance(failure.value, HttpError):
			response = failure.value.response
			self.logger.error('error %s %d', response.url, response.status)

	def parse_list(self,response):
		repeat_counts = 0
		data = json.loads(response.body)
		for each in data['subjects']:
			detail_url = each['url']
			if repeat_counts > 10:
				return
			else:
				if detail_url not in self.blfilter:
					self.blfilter.add(detail_url)
					yield scrapy.Request(url=detail_url,callback=self.parse_detail,headers=self.headers,errback=self.parse_error)
				else:
					repeat_counts += 1
					print "current url is crawled :"+detail_url


	def parse_detail(self,response):
		print "detail url:"+response.url
		_name = response.css('div#content h1 span:first-child').xpath('.//text()').extract()[0]
		name = _name
		score = response.css('div#interest_sectl div.rating_self strong.rating_num').xpath('.//text()').extract()[0]
		_summary = response.css('div.related-info div.indent span').xpath('.//text()').extract()[0]
		summary = _summary.strip()
		_actors = response.css('div#info span.actor span.attrs a').xpath('.//text()').extract()
		_types = response.css('div#info >span[property="v:genre"]').xpath('.//text()').extract()
		release_time = response.css('div#info >span[property="v:initialReleaseDate"]').xpath('.//text()').extract()[0]
		if _types:
			types = ','.join(_types)
		else:
			types = None
		if _actors:
			actors = ','.join(_actors)
		else:
			actors = None
		# print name.encode('utf-8')
		# print score
		# print summary.encode('utf-8')
		# print actors.encode('utf-8')
		# print types.encode('utf-8')
		# print release_time.encode('utf-8')
		item = DoubanSpiderItem()
		item['name'] = name
		item['score'] = score
		item['summary'] = summary
		item['types'] = types
		item['actors'] = actors
		item['src_url'] = response.url
		item['release_time'] = release_time
		yield item