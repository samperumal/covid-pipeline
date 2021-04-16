import scrapy

import datetime
import os
import dateutil.parser

class MyItem(scrapy.Item):
		# ... other item fields ...
		file_urls = scrapy.Field()
		files = scrapy.Field()
		out_dir = scrapy.Field()

class UpdatesSpider(scrapy.Spider):
		name = "updates"
		start_urls = [
				'https://sacoronavirus.co.za/category/press-releases-and-notices/'
		]

		def parse(self, response):
			for a in response.css('#posts-container article a.fusion-rollover-title-link'):
				yield response.follow(a, callback=self.parse_update)

			# yield from response.follow_all(response.css("a.pagination-next"), callback=self.parse)

		def parse_update(self, response):
			date = response.css('article.post div.fusion-meta-info span.rich-snippet-hidden::text').get()
			dt = dateutil.parser.isoparse(date)

			outdir = f'{dt.strftime("%d %B %Y")}'
			
			file_urls = response.css('article.post img::attr(src)').getall()
			
			item = MyItem()
			item['out_dir'] = outdir
			item['file_urls'] = [response.urljoin(file_url) for file_url in file_urls]
			yield item