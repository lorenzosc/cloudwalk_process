import psycopg2

def add_client(db_cursor: psycopg2.extensions.cursor, client: list):
    query = f"""
            INSERT INTO clients
            VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)
            """
    try:
        db_cursor.execute(query, client)
    except Exception as e:
        print(e)

def alter_client(id: int, db_cursor: psycopg2.extensions.cursor, changes: dict):
    set_substring = ""
    values = []
    for column, value in changes.items():
        set_substring += f" {column} = %s,\n"
        values.append(value)

    set_substring = set_substring.removesuffix(",\n")
    
    query = f"""
        UPDATE clients
        SET {set_substring}
        WHERE user_id = {id};
        """
    try:
        db_cursor.execute(query, values)
        print(f"Updated client {id}")
    except Exception as e:
        print(e)

def delete_client(id: int, db_cursor: psycopg2.extensions.cursor):
    query = f"""
            DELETE
            FROM clients
            WHERE user_id = {id};
            """
    try:
        db_cursor.execute(query)
        print(f"Deleted client {id}")
    except Exception as e:
        print(e)