import requests
from requests.auth import HTTPDigestAuth
import json
import pandas as pd
from config import CONN_PATH



class FETCH_ALL_JSON:    
#
    def allfieldsfromAPI(self,top_scores,top_categories):
    
        oid= top_scores['oid']
        category_id= top_categories['category_id']
        base_url = CONN_PATH().env_path()   #whether dev or alpha - uncommented from here
        offer_api_path = '/offers/v1/offers/oid/'
# i='5N6Muwtvqg8PSjlFsRqWVO'
# j='eeb51585-6914-48bd-ad23-491f663b32bd'
        offer_resp={}

        try:
            for i in oid:
                resp_oid = requests.get(base_url+offer_api_path+i)
            #response = resp_oid.json()

            # Convert data to dict
                all_response_offer = json.loads(resp_oid.text)

            # Convert dict to string
                all_response_offer = json.dumps(all_response_offer['payload'])
                offer_resp[i]=all_response_offer

                #print (all_response)    
    
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print ('Probable issue with Offers API')

        except:
            print ('Something else went wrong in OfferAPI')

        

        #base_url = CONN_PATH().env_path()  ## Environment specific- to be retrieved , make a call to config file
        category_api_path = '/categories/v1/categories/'
        category_resp={}
      
        try:
            for n,j in enumerate(category_id,0):
                resp_oid = requests.get(base_url+category_api_path+j)
                # Convert data to dict
                all_response_category = json.loads(resp_oid.text)

                # Convert dict to string
                all_response_category = json.dumps(all_response_category['payload'])
                top_categories.loc[n,'all_json_resp']=str(all_response_category)
                #category_resp[j]=all_response_category
                
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print ('Probable issue with Category API')

        except:
            print ('Something else went wrong in CategoryAPI')

           
        return (offer_resp,top_categories)
        