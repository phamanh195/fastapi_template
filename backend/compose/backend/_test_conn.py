import sys
import time

import psycopg2

suggest_unrecoverable_after = 30
start = time.time()

while True:
    conn = None
    try:
        conn = psycopg2.connect(
            database="${POSTGRES_DB}",
            user="${POSTGRES_USER}",
            password="${POSTGRES_PASSWORD}",
            host="${POSTGRES_SERVER}",
            port="${POSTGRES_PORT}",
        )
        cursor = conn.cursor()
        sys.stdout.write("Connect to database successfully...\n")
        sys.stdout.write("PostgreSQL server information\n")
        sys.stdout.write(f"{conn.get_dsn_parameters()}\n")
        # Executing a SQL query
        cursor.execute("SELECT version();")
        # Fetch result
        record = cursor.fetchone()
        sys.stdout.write(f"You are connected to: {record}\n")
        break
    except psycopg2.DatabaseError as exc:
        sys.stderr.write("Waiting for database to become available...\n")
        if time.time() - start > suggest_unrecoverable_after:
            sys.stderr.write(
                "This is taking longer than expected. "
                "The following exception may be indicative of an unrecoverable error: '{}'\n".format(
                    exc
                )
            )
    time.sleep(1)
