# # db.py
# import mysql.connector
# from .db_config import DB_SITE_DICT

# def get_db_connection(site_key: str):
#     if site_key not in DB_SITE_DICT:
#         raise ValueError(f"DB config not found for site: {site_key}")

#     cfg = DB_SITE_DICT[site_key]

#     return mysql.connector.connect(
#         host=cfg["host"],
#         port=cfg["port"],
#         user=cfg["user"],
#         password=cfg["password"],
#         database=cfg["database"],
#         charset=cfg["charset"],
#         autocommit=cfg["autocommit"],
#         connection_timeout=cfg["connection_timeout"]
#     )