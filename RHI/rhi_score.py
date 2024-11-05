from rhi_dataset import RHI_DATASET

class RHI_SCORE():
    def generate_score(self):
        df,blacklisted_rids=RHI_DATASET().create_dataset()

        max_txn=max(df['No-of_orders_delivered'])
        df['txns_score']=df['No-of_orders_delivered']/max_txn*20

        df['restaurant_avg_rating-score']=0
        df['PercentageOrderFulfilled']=(df['No-of_orders_delivered']/df['total_order_count'])*100
        df['PercentageOrderFulfilled-score']=0


        df.loc[df['restaurant_avg_rating'] >= 3, 'restaurant_avg_rating-score'] = df['restaurant_avg_rating'] * 2
        df.loc[df['restaurant_avg_rating'] < 3, 'restaurant_avg_rating-score'] = 0

        df.loc[df['PercentageOrderFulfilled'] == 100, 'PercentageOrderFulfilled-score'] = 20
        df.loc[(97 <= df['PercentageOrderFulfilled']) & (df['PercentageOrderFulfilled'] <= 99), 'PercentageOrderFulfilled-score'] = 15
        df.loc[(94 <= df['PercentageOrderFulfilled']) & (df['PercentageOrderFulfilled'] <= 96), 'PercentageOrderFulfilled-score'] = 10
        df.loc[(90 <= df['PercentageOrderFulfilled']) & (df['PercentageOrderFulfilled'] <= 93), 'PercentageOrderFulfilled-score'] = 5
        df.loc[df['PercentageOrderFulfilled'] < 90, 'PercentageOrderFulfilled-score'] = 0

        df['score'] = (df['PLACED-ACCEPTED-AVG-SCORE'].astype(float)+ df['ACCEPTED-PREPARED-AVG-SCORE'].astype(float)+ df['PREPARED-DELIVERED-AVG-SCORE'].astype(float)+ df['restaurant_avg_rating-score'].astype(float)+ df['PercentageOrderFulfilled-score'].astype(float) + df['txns_score'].astype(float))        
        df['score'] = df['score'].round(3).astype(float)
        df = df.fillna(0)
        df.loc[df['No-of_orders_delivered'] < 3, 'score'] = 0

        return df,blacklisted_rids