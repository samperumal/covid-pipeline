import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__, ContentSettings

connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

blob_service_client = BlobServiceClient.from_connection_string(connect_str)

container_name = str("$web")

container_client = blob_service_client.get_container_client(container_name)

files = []
for f in os.scandir("/var/data/images"):
	if f.is_file() and f.name.lower().endswith(".png"):
		files.append([f.path, f"img/%s" % f.name, "image/png"])

for f in os.scandir("/var/data"):
	if f.is_file():
		files.append([f.path, f"data/%s" % f.name, "text/" + os.path.splitext(f.name)[1][1:]])

files.append(["public-html/index.html", "index.html", "text/html"])

for f in files:
	blob_client = blob_service_client.get_blob_client(container=container_name, blob=f[1])

	print("Uploading: " + f[1])

	with open(f[0], "rb") as data:
			blob_client.upload_blob(data, blob_type='BlockBlob', overwrite=True, content_settings = ContentSettings(content_type=f[2]))
