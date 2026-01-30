CREATE KEYSPACE IF NOT EXISTS pid
WITH replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};

USE pid;

CREATE TABLE IF NOT EXISTS raw_measurements (
    generator text,
    day text,
    ts timestamp,
    v1 double,
    f double,
    PRIMARY KEY ((generator, day), ts)
);