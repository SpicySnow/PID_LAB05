def save_raw(generator, ts, V1, F):
    print(f"[MOCK DB RAW] Zapisuje: {generator}, {ts}, {V1}, {F}")

def update_latest(generator, ts, V1, F):
    print(f"[MOCK DB LATEST] Aktualizuje latest: {generator}, {V1}, {F}")

def increment_count(generator, ts):
    print(f"[MOCK DB COUNTS] Inkrementuje licznik dla: {generator} w czasie {ts}")