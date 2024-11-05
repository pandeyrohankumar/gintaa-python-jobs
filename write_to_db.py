class INSERT_TO_DB():
        def write_to_db(self,connection,all_response_offer,all_response_category):

            cursor = connection.cursor()
            
            cursor.execute("TRUNCATE TABLE gintaa_statistics.trending_offer")
            try:
                for row1 in all_response_offer.items():
                    sql = "INSERT INTO gintaa_statistics.trending_offer (oid,all_json_resp) VALUES (%s,%s)"
                    cursor.execute(sql, tuple(row1))
                connection.commit()
            except:
                print ("Issue in write to Trending Offer db.Error row is {}".format(row1))
                
            cursor2 = connection.cursor()
            cursor2.execute("TRUNCATE TABLE gintaa_statistics.popular_categories")
            try:
                for i,row2 in all_response_category.iterrows():
                    sql2 = "INSERT INTO gintaa_statistics.popular_categories (category,item_type,cumlt_dod_score,category_id,all_json_resp) VALUES (%s,%s,%s,%s,%s)"
                    cursor2.execute(sql2, tuple(row2))
                connection.commit()
            except:
                print ("Issue in write to Popular Categories db.Error row is \n {}".format(row2))
                
            message= "Write to DB done"
            return message