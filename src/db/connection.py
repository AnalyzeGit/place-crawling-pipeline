from sqlalchemy import create_engine

def get_engine(conn_uri: str):
    return create_engine(conn_uri)
