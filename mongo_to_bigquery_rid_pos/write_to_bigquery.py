from config import ConnPath
import pandas as pd


class WriteToBigquery():
    def write_to_bq(self,df):
        
        client ,bq_table_name=ConnPath().big_query_conn()

        try:
            query = f"TRUNCATE TABLE `{bq_table_name}`"

            truncate = client.query(query)
            truncate.result()

        except Exception as e:
            print(f"An error occurred: {str(e)}")

        df['rid']=df["rid"].astype(str)
        df['platform']=df["platform"].astype(str)
        
        rows_to_insert = df.to_dict(orient='records')
        
        client.insert_rows_json(bq_table_name, rows_to_insert)
        
        return 'Write to BQ Done'
