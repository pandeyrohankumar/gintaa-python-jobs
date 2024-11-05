
import pandas as pd
import numpy as np

class CALCULATE_TRENDING:
    def score_calc(self, my_df):

        #Calculate the number of days an item is available on platform
        my_df= my_df.sort_values(['oid', 'posting_date'], ascending = True)
        my_df['day_available'] = my_df.groupby(['oid']).cumcount() + 1
        

        # For a given Offer sort them in asc order of days available
        my_df.sort_values(ascending = True, by = ['oid','day_available'],inplace=True)
        my_df=my_df.reset_index().drop(columns='index',axis=1)

        # Calculate the weighted score based on various factors
        my_df['wt_raw_score']=22*my_df['chat_count']+15*my_df['comment_count']+37*my_df['deal_count']+ 15*my_df['favourite_count']+11*my_df['view_count']

        # Calculate the day-on-day increase in the weighted score 
        my_df['dod_increase']=(my_df['wt_raw_score']-my_df['wt_raw_score'].shift(1))/(my_df['wt_raw_score'].shift(1))

        #removing infinity or nan values; assigning the negative most possible for 2 days
        for i in range(len(my_df['dod_increase'])):
            if (np.isnan(my_df['dod_increase'][i])) or (my_df['dod_increase'][i] == np.inf) or (my_df['dod_increase'][i] == -np.inf):
                my_df['dod_increase'][i]=-3

        # Day-on-day increase metric should be reset to zero for the 1st day of every offer id
        for j in range(0,len(my_df)):
            if (my_df['day_available'][j]==1) :
                my_df['dod_increase'][j]=0
            else:
                pass

        # Taking the cumulative sum of the day-of-day increase by OFFER ID
        my_df['cumlt_dod_score'] = my_df.groupby(['oid'])['dod_increase'].apply(lambda x: x.cumsum())

        # Creating a table containing the Cumulative score for all the unique 'Available/Not sold' offer as on the n-th day 
        trending_df=(my_df[(my_df['day_available'] == 2) & (my_df['is_available'] == True)][['oid', 'item_type','category','category_id','posting_date','day_available', 'cumlt_dod_score']].reset_index().drop(columns = 'index'))

        # Sorting that table to get the top cumulative scores for TRENDING OFFERS
        trending_df= trending_df.sort_values(['item_type','cumlt_dod_score'],ascending=False)

        #Selecting 10 each from Item, Service, Auction
        trending_df_1 = (trending_df[trending_df['item_type']=='Item'].iloc[0:10])
        trending_df_2 = (trending_df[trending_df['item_type']=='Service'].iloc[0:10])
        trending_df_3 = (trending_df[trending_df['item_type']=='Auction'].iloc[0:10])

        #Merging into final df
        top_scores = pd.concat([trending_df_1,trending_df_2,trending_df_3])
        
        #Grouping by category to create Popular Categories by creating 3 sub-dataframes
        final_1= top_scores.groupby('category')['item_type'].apply(lambda group_series: group_series.tolist()).reset_index()
        #To create Item_Type column as array separated by comma
        final_1['item_type']=final_1['item_type'].apply(lambda x:str(",".join(np.unique(x))))
        
        #Calculate the Cumulative Score
        final_2 = top_scores.groupby('category')['cumlt_dod_score'].sum().reset_index()
        
        #Pick the first category ID - even if there are 2 diff IDs for the same category name
        final_3= top_scores.groupby('category')['category_id'].apply(lambda group_series: group_series.tolist()).reset_index()
        #final_3['category_id']=final_3['category_id'].iloc[[0]]
        list1 = []
        for i in final_3['category_id']:
            list1.append(i[0])
        final_3['category_id'] = list1
        print(final_3)

        #Merge into one and sort them
        top_categories=pd.merge(pd.merge(final_1,final_2,on='category'),final_3,on='category')
        top_categories=top_categories.sort_values(['cumlt_dod_score'],ascending=False)
        top_categories.reset_index(drop=True,inplace=True)
        ####################### Output of Top 5 Trending Offers and Popular Categories #########################


        top_scores= top_scores.head(30)
        top_categories= top_categories.head(30)

        return top_scores, top_categories
        
