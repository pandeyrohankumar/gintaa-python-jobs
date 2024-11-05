import psycopg2
from config import ConnPath


class WriteDb():
    @staticmethod
    def write_to_user_food_recommendation_type(df):
        sql_connect=ConnPath().food_listing_sql_config()
        conn = psycopg2.connect(database=sql_connect["database"], user = sql_connect["user"], password = sql_connect["password"], host = sql_connect["host"], port = sql_connect["port"])
        con = conn.cursor()

        for row in df.index:
            
            query = """
                INSERT INTO gintaa_food_listing.user_food_recommendation (uid, veg_count, non_veg_count, egg_count, other_count)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (uid) DO UPDATE
                SET
                    veg_count = COALESCE(gintaa_food_listing.user_food_recommendation.veg_count, 0) + COALESCE(EXCLUDED.veg_count, 0),
                    non_veg_count = COALESCE(gintaa_food_listing.user_food_recommendation.non_veg_count, 0) + COALESCE(EXCLUDED.non_veg_count, 0),
                    egg_count = COALESCE(gintaa_food_listing.user_food_recommendation.egg_count, 0) + COALESCE(EXCLUDED.egg_count, 0),
                    other_count = COALESCE(gintaa_food_listing.user_food_recommendation.other_count, 0) + COALESCE(EXCLUDED.other_count, 0);
            """

            k = (str(df["uid"][row]),int(df["veg_count"][row]),int(df["non_veg_count"][row]),int(df["egg_count"][row]), int(df["other_count"][row]))

            con.execute(query,k)
        conn.commit()  
                
        message= "Write to User Veg Non_veg done"
        return message
    
    @staticmethod
    def write_to_popular_foods(df):
        sql_connect=ConnPath().food_listing_sql_config()
        conn = psycopg2.connect(database=sql_connect["database"], user = sql_connect["user"], password = sql_connect["password"], host = sql_connect["host"], port = sql_connect["port"])
        con = conn.cursor()

        for row in df.index:
            
            query = """
                INSERT INTO gintaa_food_listing.popular_foods (id,food_listing_id, rid, cuisine,score)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    rid = EXCLUDED.rid,
                    cuisine = EXCLUDED.cuisine,
                    score = EXCLUDED.score;
            """
            k = (str(df["food_listing_id"][row]),str(df["food_listing_id"][row]),str(df["rid"][row]),str(df["cuisine"][row]), float(df["score"][row]))

            con.execute(query,k)  

        conn.commit()  
            
                
        message= "Write to Popular Food done"
        return message
    
    @staticmethod
    def write_to_user_food_recommendation_cuisine(df):
        sql_connect=ConnPath().food_listing_sql_config()
        conn = psycopg2.connect(database=sql_connect["database"], user = sql_connect["user"], password = sql_connect["password"], host = sql_connect["host"], port = sql_connect["port"])
        con = conn.cursor()

        for row in df.index:
            
            query = """
                INSERT INTO gintaa_food_listing.user_food_recommendation (uid, cuisine)
                VALUES (%s, %s)
                ON CONFLICT (uid) DO UPDATE SET
                    cuisine = EXCLUDED.cuisine;
            """
            k = (str(df["uid"][row]),str(df["cuisine"][row]))

            con.execute(query,k)  

        conn.commit()  
                
        message= "Write to User Cuisine done"
        return message