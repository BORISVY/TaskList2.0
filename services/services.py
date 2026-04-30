from data.db import connect
from contextlib import contextmanager

@contextmanager
def connection():
    conn = connect()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()