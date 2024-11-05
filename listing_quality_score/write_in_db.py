import psycopg2
from config import CONN_PATH
class WRITE_IN_DB():
    def update_db(self,df):
        sql_connect=CONN_PATH().init_config()
        conn = psycopg2.connect(database=sql_connect["database"], user = sql_connect["user"], password = sql_connect["password"], host = sql_connect["host"], port = sql_connect["port"])


        con = conn.cursor()   
        # con.execute("TRUNCATE TABLE gintaa_statistics.listing_score")
        
        for row in df.index:

            sql = "UPDATE gintaa_statistics.offer_statistics SET score = %s WHERE oid = %s"
            k=(str(df["score"][row]),str(df["oid"][row]))
            con.execute(sql,k)  

            sql2 = """
                INSERT INTO gintaa_statistics.listing_score 
                    (oid, name_count_score, facets_in_name_score, desc_count_score, facets_in_desc_score, 
                     image_count_score, optional_tag_count_score, freeshipping_score, cod_score, 
                     returnable_score, video_score, score)
                VALUES 
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (oid) DO UPDATE SET
                    name_count_score = EXCLUDED.name_count_score,
                    facets_in_name_score = EXCLUDED.facets_in_name_score,
                    desc_count_score = EXCLUDED.desc_count_score,
                    facets_in_desc_score = EXCLUDED.facets_in_desc_score,
                    image_count_score = EXCLUDED.image_count_score,
                    optional_tag_count_score = EXCLUDED.optional_tag_count_score,
                    freeshipping_score = EXCLUDED.freeshipping_score,
                    cod_score = EXCLUDED.cod_score,
                    returnable_score = EXCLUDED.returnable_score,
                    video_score = EXCLUDED.video_score,
                    score = EXCLUDED.score
            """
            l = (str(df["oid"][row]), safe_float(df["nameCount_score"][row]), safe_float(df["facetsInName_score"][row]), safe_float(df["descCount_score"][row]), safe_float(df["facetsInDesc_score"][row]), safe_float(df["imageCount_score"][row]), safe_float(df["optionalTagCount_score"][row]), safe_float(df["freeShipping_score"][row]), safe_float(df["COD_score"][row]), safe_float(df["returnable_score"][row]), safe_float(df["video_score"][row]), safe_float(df["score"][row]))
            con.execute(sql2,l)

        conn.commit()

        return "Done"
    
def safe_float(value):
    if value:
        return float(value)
    else:
        return None