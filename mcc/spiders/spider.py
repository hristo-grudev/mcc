import scrapy

from scrapy.loader import ItemLoader
from ..items import MccItem
from itemloaders.processors import TakeFirst


class MccSpider(scrapy.Spider):
	name = 'mcc'
	start_urls = ['https://www.mcc.it/primopiano/notizie/']

	def parse(self, response):
		post_links = response.xpath('//h2/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="pagination-next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)


	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="post-content"]/div/div/div/div/div/div//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="mcc-data-notizia"]/text()').get()

		item = ItemLoader(item=MccItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
