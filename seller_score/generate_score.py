import pandas as pd
from datetime import date
from dateutil import relativedelta
from create_data_set import CREATE_DATASET


class GENERATE_SCORE():
    def gen_score(self):
        time_df=CREATE_DATASET().avg_time()
        rating_reg_df=CREATE_DATASET().rating()
        df=pd.merge(time_df,rating_reg_df , on='receiving_user_id', how='left')
        df["no_of_months"]=""
        for i in df.index:
            try:
                delta=relativedelta.relativedelta(date.today(),df["reg_date"][i])
                if(delta.months<1):
                    df["no_of_months"][i]=1
                else:
                    df["no_of_months"][i]=delta.months
            except:
                df["no_of_months"][i]=1
        df["avg_trans"]=""
        for i in df.index:
            df["avg_trans"][i]=int(df["Number of Products Sold"][i])/int(df["no_of_months"][i])

        df['reg_date'] = df['reg_date'].dt.date
        df["score1"]=""
        df["score2"]=""
        df["score3"]=""
        df["score4"]=""
        df["score5"]=""
        df["score6"]=""
        df["score"]=""

        max=df["avg_trans"].max()
        for i in df.index:
            
            
            score1=df["avg_trans"][i]/max*30
            df["score1"][i]=score1


        
            score2=0
            k=0
            if df["Average Time ACCEPTED from INITIATED state in Hours"][i]<6:
                score2+=50/50*20
                k=50
            elif 6<=df["Average Time ACCEPTED from INITIATED state in Hours"][i]<12:
                score2+=40/50*20
                k=40
            elif 12<=df["Average Time ACCEPTED from INITIATED state in Hours"][i]<24:
                score2+=20/50*20
                k=20
            elif df["Average Time ACCEPTED from INITIATED state in Hours"][i]>=24:
                score2+=10/50*20
                k=10
            df["score2"][i]=score2
        
        
            score3=0
            if df["Avg Hours to ACCEPTED from REVISED state"][i]<6:
                score3+=50/50*10
            elif 6<=df["Avg Hours to ACCEPTED from REVISED state"][i]<12:
                score3+=40/50*10
            elif 12<=df["Avg Hours to ACCEPTED from REVISED state"][i]<24:
                score3+=20/50*10
            elif df["Avg Hours to ACCEPTED from REVISED state"][i]>=24:
                score3+=10/50*10
            if (score3==0):
                score3=(k/50*10)

            df["score3"][i]=score3

        


            score4=0
            if df["Avg Hours to CLOSED from PARTIAL_CLOSED state"][i]<24:
                score4+=60/60*15
            elif 24<=df["Avg Hours to CLOSED from PARTIAL_CLOSED state"][i]<48:
                score4+=50/60*15
            elif 48<=df["Avg Hours to CLOSED from PARTIAL_CLOSED state"][i]<72:
                score4+=40/60*15
            elif df["Avg Hours to CLOSED from PARTIAL_CLOSED state"][i]>=72:
                score4+=20/60*15
            df["score4"][i]=score4


            score5=0
            if df["Avg Hours to PARTIAL_CLOSED from ACCEPTED state"][i]<24:
                score5+=50/50*15
            elif 24<=df["Avg Hours to PARTIAL_CLOSED from ACCEPTED state"][i]<48:
                score5+=40/50*15
            elif 48<=df["Avg Hours to PARTIAL_CLOSED from ACCEPTED state"][i]<72:
                score5+=30/50*15
            elif df["Avg Hours to PARTIAL_CLOSED from ACCEPTED state"][i]>=72:
                score5+=10/50*15
            df["score5"][i]=score5

            score6=0
            df["score6"][i]=df["user_rating"][i]*2

            score=score1+score2+score3+score4+score5+score6
            df["score"][i]=round(score,3)

        return df