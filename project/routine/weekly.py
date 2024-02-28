from ..utils.connect import connect
import subprocess
import datetime
from ..utils.config import load_config

if __name__ == "__main__":
    conn = connect()
    cur = conn.cursor()
    
    # Check data volume
    query = "SELECT pg_size_pretty( pg_database_size(%s) );"
    dbname = "cloudwalk_process"
    cur.execute(query, [dbname])
    print(f"Current database size is {cur.fetchone()[0]}")

    # Make a backup
    config = load_config()
    backup_file = f'backup_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.sql'

    pg_dump_cmd = [
        'pg_dump',
        '-h', config["host"],
        '-p', '5432',
        '-U', config["user"],
        '-d', config["database"],
        '-Fc',
        '-f', backup_file
    ]

    try:
        subprocess.run(pg_dump_cmd, check=True)
        print(f'Backup successful. File: {backup_file}')
    except subprocess.CalledProcessError as e:
        print(f'Error during backup: {e}')

    cur.close()
    conn.close()

