from write_in_db import WRITE_IN_DB
from listing_score_calculate import LISTING_SCORE_CALCULATE

import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

df=LISTING_SCORE_CALCULATE().name_desc_count()
score_df=LISTING_SCORE_CALCULATE().generate_score(df)
final_score_df=LISTING_SCORE_CALCULATE().remove_hidden(score_df)

# final_score_df=final_score_df[['oid','score']]
print(WRITE_IN_DB().update_db(final_score_df))