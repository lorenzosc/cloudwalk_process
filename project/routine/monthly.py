from ..utils.connect import connect
import subprocess
import datetime
import sys
from ..utils.config import load_config

if __name__ == "__main__":
    conn = connect()
    cur = conn.cursor()

    # setup backup
    config = load_config()
    backup_file = sys.argv[1]

    pg_restore_cmd = [
        'pg_restore',
        '-h', config["host"],
        '-p', '5432',
        '-U', config["user"],
        '-d', config["database"]+"_backup",
        backup_file
    ]

    # Run the pg_restore command
    try:
        subprocess.run(pg_restore_cmd, check=True)
        print(f'Restore successful from {backup_file}')
    except subprocess.CalledProcessError as e:
        print(f'Error during restore: {e}')

    # Check if backup isn't corrupted
    try:
        conn_db = connect(config["database"]+"_backup")
        cur_db = conn_db.cursor()
        print("Proceding to vacuum backup database")
        conn_db.autocommit = True
        cur_db.execute("VACUUM FULL")
        print("Vacuum done sucessfully")

    except Exception as e:
        print(e)
        print("There was a problem in backup file database connection, the backup file could be corrupted")

    finally:
        cur_db.execute(f"DROP TABLE loans; DROP TABLE clients;")
        conn_db.commit()
        cur_db.close()
        conn_db.close()


    # Index maintenance
    conn.autocommit = True
    cur.execute(f"REINDEX DATABASE {config['database']}")
    cur.execute("VACUUM ANALYZE")
    cur.execute("CLUSTER")
    
    conn.commit()
    cur.close()
    conn.close()