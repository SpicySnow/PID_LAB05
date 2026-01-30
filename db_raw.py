from cassandra.cluster import Cluster
from datetime import datetime

CASSANDRA_HOSTS = ["cassandra"]
KEYSPACE = "pid"

cluster = Cluster(CASSANDRA_HOSTS)
session = cluster.connect(KEYSPACE)

stmt_save = session.prepare("""
    INSERT INTO raw_measurements (generator, day, ts, v1, f)
    VALUES (?, ?, ?, ?, ?)
""")


def save_raw(generator: str, ts: datetime, v1: float, f: float):
    """
    Zapisuje surowy pomiar do historii.
    Kolumna 'day' jest wyliczana automatygcznie z 'ts'.
    """
    # dzień z timestampu jako klucz partycji
    day_str = ts.strftime('%Y-%m-%d')

    session.execute(stmt_save, (generator, day_str, ts, v1, f))
