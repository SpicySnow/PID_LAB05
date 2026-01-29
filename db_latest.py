from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from datetime import datetime

CASSANDRA_HOSTS = ["cassandra"]  # nazwa serwisu z docker-compose
KEYSPACE = "pid"

cluster = Cluster(CASSANDRA_HOSTS)
session = cluster.connect(KEYSPACE)

stmt_update = session.prepare("""
    INSERT INTO latest (generator, ts, v1, f)
    VALUES (?, ?, ?, ?)
""")

stmt_get = session.prepare("""
    SELECT generator, ts, v1, f
    FROM latest
    WHERE generator = ?
""""

def update_latest(generator: str, ts: datetime, v1: float, f: float):
    """
    Aktualizuje ostatnie wartości V1 i F dla generatora.
    Nadpisuje poprzedni rekord.
    """
    session.execute(stmt_update, (generator, ts, v1, f))


def get_latest(generator: str):
    """
    Zwraca ostatnie wartości V1 i F dla generatora.
    """
    row = session.execute(stmt_get, (generator,)).one()
    if row is None:
        return None

    return {
        "generator": row.generator,
        "ts": row.ts,
        "V1": row.v1,
        "F": row.f
    }


