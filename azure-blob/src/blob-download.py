import os
import re
import datetime
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__, ContentSettings

log_path = "/var/data/download/log.json"

def download_log():

	connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

	blob_service_client = BlobServiceClient.from_connection_string(connect_str)
	blob_client = blob_service_client.get_blob_client("covid", "log.json")

	with open(log_path, "wb") as my_blob:
		download_stream = blob_client.download_blob()
		my_blob.write(download_stream.readall())
		my_blob.write("null]\n".encode())

def strip_port(ip):
	return re.search(r"\d+\.\d+\.\d+\.\d+", ip)[0]

def parse_log():
	import json

	req_list = []

	with open (log_path, "r") as input_file:
		json_array = json.load(input_file)
		
		for item in json_array:
			if item is not None:
				req = item['req']
				headers = req['headers']

				details = {
					'date': str(datetime.datetime.fromisoformat(item['date'].replace('Z', '+00:00')).date()),
					'datetime': item['date'],
					'ip': strip_port(headers['client-ip']),
					'ips' : [strip_port(headers['client-ip'])] + [strip_port(x) for x in headers['x-forwarded-for'].split(",")],
					'agent' : re.findall(r"[^ ]+/[^ ]+", headers['user-agent']),
					'agent-detail' : re.findall(r"\([^)]+\)", headers['user-agent'])
				}

				req_list.append(details)

	print(req_list[0:5])

	with open("/var/data/download/small_log.json", "w") as output_file:
		json.dump(req_list, output_file, indent = 2)

os.makedirs("/var/data/download", exist_ok=True)

download_log()
parse_log()