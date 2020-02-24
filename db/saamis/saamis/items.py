# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SaamisItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	Name = scrapy.Field()
	Country = scrapy.Field()
	City = scrapy.Field()
	GlobalRank=scrapy.Field()
	GlobalScore=scrapy.Field()
	Summary=scrapy.Field()
	Address = scrapy.Field()
	Website = scrapy.Field()
	data_long= scrapy.Field()
	data_lat = scrapy.Field()
	data_url = scrapy.Field()
	students = scrapy.Field()
	international_students = scrapy.Field()
	academic_staff = scrapy.Field()
	international_staff = scrapy.Field()
	ud_awarded = scrapy.Field()
	md_awarded = scrapy.Field()
	dd_awarded = scrapy.Field()
	research_only_staff = scrapy.Field()
	new_undergraduate_students = scrapy.Field()
	new_masters_students = scrapy.Field()
	new_doctoral_students = scrapy.Field()
	more_information = scrapy.Field()
	indicator_rankings = scrapy.Field()
	subject_rankings = scrapy.Field()