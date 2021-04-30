import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

blob_service_client = BlobServiceClient.from_connection_string(connect_str)

container_name = str("covid")

container_client = blob_service_client.get_container_client(container_name)

files = []
for f in os.scandir("/var/data/images"):
	if f.is_file() and f.name.lower().endswith(".png"):
		files.append(f.path)

for f in os.scandir("/var/data"):
	if f.is_file():
		files.append(f.path)

for filepath in files:
	blob_client = blob_service_client.get_blob_client(container=container_name, blob=filepath)

	print("Uploading: " + filepath)

	with open(filepath, "rb") as data:
			blob_client.upload_blob(data, overwrite=True)