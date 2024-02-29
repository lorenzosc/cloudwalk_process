import psycopg2
from .config import load_config

def connect(db_name = None) -> psycopg2.extensions.connection:
    """Connect to the PostgreSQL database server

    :param config: database configuration
    :return: connection to da
    """
    config = load_config()
    if db_name is not None:
        config['database'] = db_name
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


if __name__ == '__main__':
    connect()