#!/bin/bash

function db_ready() {
    python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname="uks_db", user="uks", password="uks", host="db")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until db_ready; do
    >&2 echo "Database isn't available. Waiting..."
    sleep 1
done

>&2 echo "Database is available."

./start_app.sh