import os
import re

def try_parse_int(s, base=10, val=None):
	try:
		return int(s, base)
	except ValueError:
		return val

def try_parse_float(s, base=10, val=None):
	try:
		return float(s)
	except ValueError:
		return val

def process(path, o):
	output_path = re.sub("\..*\.txt", ".csv", path)

	with open(path, "r") as f:
		for line in f.readlines():
			m = re.search(r"^([a-zA-Z\W]+)\W+(\d+)\W+(\d.+)$", line)
			if m is not None:
				print("\t".join([
					m[1], 
					str(try_parse_int(m[2], val="")), 
					str(try_parse_float(m[3].replace(",", "."), val="")), 
					path
				]), file = o)

def process_sub_directories(root_path):
	with open(os.path.join(root_path, "combined.tsv"), "w") as o:
		for d in os.scandir(root_path):
			if d.is_dir():
				for f in os.scandir(d.path):
					if f.is_file() and f.name.lower().endswith(".txt"):
						m = re.search("-table-1\..*\.txt$", f.path)
						if m is not None:
							process(f.path, o)

def main():
	root_path = os.environ['SCRAPY_DATA_PATH'] = os.environ['SCRAPY_DATA_PATH']

	process_sub_directories(root_path)

if __name__ == "__main__":
		main()
