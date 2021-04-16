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
