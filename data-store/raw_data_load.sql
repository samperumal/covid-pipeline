DROP TABLE IF EXISTS raw_data;
CREATE TABLE raw_data(
	province VARCHAR,
	total INT,
	[percent] FLOAT NULL,
	source VARCHAR
);

COPY raw_data FROM '/var/data/sacorona/images/combined.tsv' 
	DELIMITER E'\t'
	NULL '';