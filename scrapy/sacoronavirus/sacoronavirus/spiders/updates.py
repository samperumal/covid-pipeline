import scrapy

import datetime
import os
import dateutil.parser

from .. import items


class UpdatesSpider(scrapy.Spider):
		name = "updates"
		start_urls = [
				'https://sacoronavirus.co.za/category/press-releases-and-notices/'
		]

		def parse(self, response):
			for a in response.css('#posts-container article a.fusion-rollover-title-link'):
				yield response.follow(a, callback=self.parse_update)

			yield from response.follow_all(response.css("a.pagination-next"), callback=self.parse)

		def parse_update(self, response):
			# self.logger.debug("Response Url: " + response.url)
			item = items.SacoronavirusItem()
			
			date = response.css('article.post div.fusion-meta-info span.rich-snippet-hidden::text').get()
			dt = dateutil.parser.isoparse(date)

			outdir = f'{dt.strftime("%d %B %Y")}'
			self.logger.debug("Out Dir: " + outdir)

			abs_dir = os.path.join(self.settings['FILES_STORE'], outdir)

			if not os.path.isdir(abs_dir):
				try:
					self.logger.info("Creating dir: " + outdir)
					os.mkdir(abs_dir)
				except OSError as error:
					pass
			
			file_urls = response.css('article.post img::attr(src)').getall()

			table = response.css('div.post-content table.NormalTable')

			if table is not None:
				item['table_html'] = table
			else:
				item['table_html'] = None
				# self.logger.info('Table: %s' % outdir)
			
			item['out_dir'] = outdir
			item['file_urls'] = [response.urljoin(file_url) for file_url in file_urls]
			yield item