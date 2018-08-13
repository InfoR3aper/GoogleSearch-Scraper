# from __future__ import unicode_literals
import scrapy

import json

import os

import scrapy

from scrapy.spiders import Spider

from scrapy.http import FormRequest

from scrapy.http import Request

from selenium import webdriver

from chainxy.items import ChainItem

from lxml import etree

from lxml import html

import time

import pdb



class Google(scrapy.Spider):

	name = 'google'

	domain = 'https://www.google.com/'

	history = []


	def __init__(self):

		self.driver = webdriver.Chrome("./chromedriver")

	
	def start_requests(self):

		yield scrapy.Request(url=self.domain, callback=self.parse) 


	def parse(self, response):

		self.driver.get(self.domain)

		self.driver.find_element_by_id("lst-ib").send_keys("restaurants in london, UK")

		self.driver.find_element_by_name("btnK").click()

		self.driver.find_elements_by_xpath('//div[contains(@class, "AEprdc vk_c")]//a')[0].click()

		next_bt = self.driver.find_element_by_id('pnnext')

		while (next_bt != None) :

			loc_list = self.driver.find_elements_by_class_name('VkpGBb')

			for loc in loc_list:

				try:

					loc.click()

					time.sleep(1)

					source = self.driver.page_source.encode("utf8")

					tree = etree.HTML(source)

					detail = ''.join(self.eliminate_space(tree.xpath('//div[@class="SALvLe"]//text()')))

					item = ChainItem()

					item['address'] = detail.split('Address:')[1].split('Hours:')[0].strip()

					item['phone'] = detail.split('Phone:')[1].replace('+','').replace(' ', '').strip()

					yield item

				except:

					pass

			next_bt = self.driver.find_element_by_id('pnnext')

			next_bt.click()

			time.sleep(3)


	def validate(self, item):

		try:

			return item.replace('\n', '').replace('\t','').replace('\r', '').strip()

		except:

			pass


	def eliminate_space(self, items):

	    tmp = []

	    for item in items:

	        if self.validate(item) != '':

	            tmp.append(self.validate(item))

	    return tmp