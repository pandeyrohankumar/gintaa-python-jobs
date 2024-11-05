import psycopg2
from config import CONN_PATH
import pandas as pd




sql_connect=CONN_PATH().stats_sql_config()
conn = psycopg2.connect(database=sql_connect["database"], user = sql_connect["user"], password = sql_connect["password"], host = sql_connect["host"], port = sql_connect["port"])

cursor = conn.cursor()
cursor.execute("drop table gintaa_statistics.popularity_score")
conn.commit()
# create_table ="CREATE TABLE gintaa_statistics.popularity_score(oid VARCHAR(225),popularity_score VARCHAR(225));"
# cursor.execute(create_table)
# conn.commit()

print("Table created")