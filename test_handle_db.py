from connect import connect
from config import load_config
from datetime import datetime
from handle_db import add_client, alter_client, delete_client

if __name__ == "__main__":

    config = load_config()
    conn = connect(config)
    cursor = conn.cursor()

    chosen_date = datetime(2020, 4, 24, 17, 52, 12)
    changes = {"batch": 1, "status": "approved", "interest_rate": 70}
    client = [90001, chosen_date, "denied",
              5, 52500, 65, None,
              chosen_date]
    
    alter_client(90000, cursor, changes)
    delete_client(90001, cursor)
    add_client(cursor, client)

    conn.commit()
    cursor.close()
    conn.close()