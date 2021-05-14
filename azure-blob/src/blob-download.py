import os
import re
import datetime
import shutil
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__, ContentSettings

folder_path = "/var/data/download"

def download_log(blob_name = "log.json"):

	connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

	blob_service_client = BlobServiceClient.from_connection_string(connect_str)
	blob_client = blob_service_client.get_blob_client("covid", blob_name)
	file_path = os.path.join(folder_path, blob_name)
	file_size = os.path.getsize(file_path) if os.path.isfile(file_path) else 0
	blob_size = blob_client.get_blob_properties().size
	length = blob_size - file_size

	if length <= 0: 
		print("Blob '%s' already downloaded." % (blob_name))
		return

	print("Downloading blob '%s' at offset %d with length %d to '%s'" % (blob_name, file_size, length, file_path))

	download_stream = blob_client.download_blob(file_size, length)
	
	with open(file_path, "ab") as my_blob:
		my_blob.write(download_stream.readall())

	fixed_path = os.path.join(folder_path, "complete-" + blob_name)

	shutil.copyfile(file_path, fixed_path)

	with open(fixed_path, "a") as my_blob:
		my_blob.write("null]\n")

def strip_port(ip):
	return re.search(r"\d+\.\d+\.\d+\.\d+", ip)[0]

def parse_log(blob_name = "complete-log.json"):
	import json

	req_list = []

	print("Parsing log file to smaller version")

	with open (os.path.join(folder_path, blob_name), "r") as input_file:
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

	with open(os.path.join(folder_path, "small_log.json"), "w") as output_file:
		json.dump(req_list, output_file, indent = 2)
		output_file.write("\n")

os.makedirs(folder_path, exist_ok=True)

download_log()
parse_log()