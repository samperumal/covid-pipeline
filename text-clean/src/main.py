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

def process_txt(path, o):
	output_path = re.sub("\..*\.txt", ".csv", path)

	with open(path, "r") as f:
		for line in f.readlines():
			m = re.search(r"^([a-zA-Z\W]+)\W+(\d+)\W+(\d.+)$", line)
			if m is not None:
				d = re.search(r"/var/data/sacorona/images/(.+)/.+", path)
				print("\t".join([
					m[1], 
					str(try_parse_int(m[2], val="")), 
					str(try_parse_float(m[3].replace(",", "."), val="")), 
					path,
					d[1]
				]), file = o)

def process_table(path, o):
	with open(path, "r") as f:
		for line in f.readlines():
			# m = re.search(r"^([a-zA-Z\W]+)\W+(\d+)\W+(\d.+)$", line)
			line = line.strip()#.replace(",", ".")
			line = re.sub(r"(\d)\W(\d)", "$1$2", line)
			parts = line.split("\t")
			d = re.search(r"/var/data/sacorona/images/(.+)/.+", path)
			if parts[0].lower().strip() not in ["eastern cape",
"free state",
"gauteng",
"kwazulu-natal",
"limpopo",
"mpumalanga",
"north west",
"northern cape",
"western cape"]: continue
			while len(parts) < 3: 
				parts.append("0")
				line += "\t0"
			print("\t".join([x for x in parts[0:3]]) + f"\t%s\t%s" % (path, d[1]), file = o)

def process_sub_directories(root_path):
	with open(os.path.join(root_path, "combined.tsv"), "w") as o:
		for d in os.scandir(root_path):
			if d.is_dir():
				for f in os.scandir(d.path):
					if f.is_file() and f.name.lower().endswith(".txt"):
						m = re.search("-table-1\..*\.txt$", f.path)
						if m is not None:
							process_txt(f.path, o)
					if f.is_file() and f.name.lower().endswith(".tsv"):
						m = re.search("table-1\.tsv$", f.path)
						if m is not None:
							process_table(f.path, o)

import psycopg2
def load_into_db():
	try:
		conn = psycopg2.connect(
			host=os.environ['POSTGRES_HOST_NAME'],
			database="sacorona",
			user=os.environ['POSTGRES_USER_NAME'],
			password=os.environ['POSTGRES_PASSWORD']
		)

		# create a cursor
		cur = conn.cursor()

		print(os.getcwd())
				
		# execute a statement
		print('Running load')
		cur.execute(open("src/raw_data_load.sql", "r").read())
		
		# close the communication with the PostgreSQL
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
			print('Database connection closed.')

def main():
	root_path = os.environ['SCRAPY_DATA_PATH'] = os.environ['SCRAPY_DATA_PATH']

	process_sub_directories(root_path)

	# load_into_db()

if __name__ == "__main__":
		main()
