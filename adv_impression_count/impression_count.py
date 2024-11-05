import pandas as pd
from config import CONN_PATH


class IMPRESSION():

  def impression_count(self):
    client,bq_table_name=CONN_PATH().big_query_conn()
    query_job1 = client.query(f"""
    SELECT platform,eq.value.string_value,Count(eq.value.string_value) as impr_count  FROM `{bq_table_name}.events_*`, UNNEST(event_params) eq where event_name='gintaa_ad_impression_banner' AND _TABLE_SUFFIX BETWEEN FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 14 DAY)) AND FORMAT_DATE('%Y%m%d', CURRENT_DATE())  and eq.key='sponsored_by' group by 2,1 """)

    bq_view_df = query_job1.result().to_dataframe()
    bq_view_df=bq_view_df.drop(['platform'], axis=1)
    groups=bq_view_df.groupby(['string_value'])['impr_count'].sum()

    adv=[]
    impr=[]
    for idx in groups.index:
      adv.append(idx)
      impr.append(groups[idx])
    
    df = pd.DataFrame(list(zip(adv, impr)),columns =['string_value', 'impr_count'])

    return df




    