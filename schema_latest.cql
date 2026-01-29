CREATE KEYSPACE IF NOT EXISTS pid
WITH replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};

USE pid;

CREATE TABLE IF NOT EXISTS latest (
    generator text PRIMARY KEY,
    ts timestamp,
    v1 double,
    f double
);
