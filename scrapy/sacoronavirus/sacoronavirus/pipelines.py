# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import os
from urllib.parse import urlparse
import logging

class SacoronavirusPipeline(FilesPipeline):
	def file_path(self, request, response=None, info=None, *, item=None):
		adapter = ItemAdapter(item)
		path = os.path.basename(urlparse(request.url).path)
		path = os.path.join(adapter['out_dir'], path)
		# logging.warning(f"Output to: {path}")
		return path

import json

class HtmlTablePipeline:

	# def open_spider(self, spider):
	# 		self.file = open('items.jl', 'w')

	# def close_spider(self, spider):
	# 		self.file.close()

	def process_item(self, item, spider):
			adapter = ItemAdapter(item)
			html = adapter.get('table_html')
			if html is not None:
				# line = json.dumps(ItemAdapter(item).asdict()) + "\n"
				i = 1
				for table in html.css("table"):
					path = os.path.join(spider.settings['FILES_STORE'], adapter['out_dir'], 'table-%i.tsv' % i)
					with open(path, "w") as file:
						# file.write(html.css('tbody::text').get())
						for tr in table.css('tr'):
							line = "\t".join(tr.css('td span::text').getall()) + "\n"
							file.write(line)
					# spider.logger.info('Table: %s' % path)
					i += 1
				pass
			return item