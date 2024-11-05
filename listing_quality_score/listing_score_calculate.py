import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from string import punctuation
from initialize_data import INITIALIZE_DATA

class LISTING_SCORE_CALCULATE():   

    def data_preprocess(self,all_data_df):
        oid = []
        img=[]
        name=[]
        desc=[]
        tag_name=[]
        tag_value=[]
        returnable=[]
        optional_tag=[]
        cod=[]
        freeShipping=[]
        offerstage=[]
        videos=[]
        price=[]
        unitOfferValuation=[]
        vertical=[]
        facets_name=[]
        facets_value=[]
        
        for x in all_data_df:
            tag={}
            facets={}
            oid.append(x["oid"])
            name.append(x["name"])
            img.append(x["images"])
            offerstage.append(x["offerStage"])
            if x.get("description") is not None:
                desc.append(x["description"])
            else:
                desc.append("null")
            category= x["category"]
            try:
                tag=category["tags"]
            except:
                print("")
            li=[]
            li2=[]
            li3=[]
            try:
                for dict in tag:
                    if dict["mandatory"]:
                        li.append(dict["name"])
                        li3.append(dict["values"])
                    else:
                        li2.append(dict["name"])
            except:
                print("")                
            tag_name.append(li)
            optional_tag.append(li2)
            tag_value.append(li3)
            facets=x["facets"]
            facets_li=[]
            facets_li2=[]
            try:
                for dict in facets:
                    if dict["mandatory"]:
                        facets_li.extend(dict["name"])
                        facets_li2.extend(dict["values"])
            except:
                print("")            
            facets_name.append(facets_li)
            facets_value.append(facets_li2)
            returnable.append(x["returnable"])
            if x.get("cod") is not None:
                cod.append(x["cod"])
            else:
                cod.append("null")
            if x.get("freeShipping") is not None:
                freeShipping.append(x["freeShipping"])
            else:                
                freeShipping.append("null")
            videos.append(x["videos"])

            if x.get("price") is not None:
                price.append(x["price"])
            else:
                price.append(x["unitOfferValuation"])
            unitOfferValuation.append(x["unitOfferValuation"])
            j=0
            for i in (x["category"]["hierarchy"]):
                if (j==0):
                    v=i["name"]
                    j+=1
                 
            vertical.append(v)
               
            
        df = pd.DataFrame(columns = ["oid","name","vertical","img" ,"offerStage","description","tags","tag_values","facets_value","facets_count_name","returnable","optional_tag","cod","freeShipping","videos","price","unitOfferValuation","gintaa_in_name","gintaa_in_desc"])
        df["oid"]=oid
        df["name"]=name
        df["img"]=img
        df["description"]=desc
        df["tags"]=tag_name
        df["tag_values"]=tag_value
        df["returnable"]=returnable
        df["optional_tag"]=optional_tag
        df["cod"]=cod
        df["freeShipping"]=freeShipping
        df["offerStage"]=offerstage
        df["videos"]=videos
        df["price"]=price
        df["unitOfferValuation"]=unitOfferValuation
        df["vertical"]=vertical
        df["facets_value"]=facets_value
        
        df["name_count"]=""
        df["description_count"]=""
        df["tags_count"]=""
        df['image_count']=""
        df["optional_tag_count"]=""
        df["discount"]=""
        df["video_count"]=""

        return df  

    def generate_counts(self,df):
        for i in df.index:
            st=df["name"][i].strip()
            count=1
            for j in st:
                if j==" ":
                    count+=1
            df["name_count"][i]=count
            if ((df["name"][i].lower()).find('gintaa') != -1):
                df["gintaa_in_name"][i]="Available"
        stop_words = stopwords.words("english")+list(punctuation)

        for i in df.index:
            tokens = word_tokenize(df["description"][i].lower())
            lemma = [WordNetLemmatizer().lemmatize(term) for term in tokens
                        if term not in stop_words]
            res = " ".join(lemma)
            df["description"][i]=res

        for i in df.index:
            st=df["description"][i].strip()
            if st=="null":
                df["description_count"][i]=0
                continue
            count=1
            for j in st:
                if j==" ":
                    count+=1
            df["description_count"][i]=count 
            if ((df["description"][i].lower()).find('gintaa') != -1 or (df["description"][i].lower()).find('ginta') != -1):
                df["gintaa_in_desc"][i]="Avalable"
        
        for i in df.index:
            df["tag_values"][i]=list(set(sum(df["tag_values"][i],[])))

        for i in df.index:
            facet_in_name=[]
            
            for k in df["tag_values"][i]:
                k=str(k)
                s=str(df["description"][i])
                if k.lower() in (s.lower()):
                    facet_in_name.append(k)
                        
            facet_in_desc=list(set(facet_in_name))
            df["tags_count"][i]=len(facet_in_desc)

        for i in df.index:
            tokens = word_tokenize(df["name"][i].lower())
            lemma = [WordNetLemmatizer().lemmatize(term) for term in tokens
                        if term not in stop_words]
            res = " ".join(lemma)
            df["name"][i]=res

        for i in df.index:
            facet_in_name=[]
            
            for k in df["facets_value"][i]:
                    k=str(k)
                    s=str(df["name"][i])
                    if k.lower() in s.lower():
                        facet_in_name.append(k)
                        
            facet_in_name=list(set(facet_in_name))
            df["facets_count_name"][i]=len(facet_in_name)

        for i in df.index:
            df["optional_tag_count"][i]=len(df["optional_tag"][i])

        for i in df.index:
            df['image_count'][i]=len(df["img"][i])

        for i in df.index:
            df['video_count'][i]=len(df["videos"][i])
            

        for i in df.index:
            df["discount"][i]=(float(df["price"][i])-float(df["unitOfferValuation"][i]))/float(df["price"][i])*100
        
        return df

    def name_desc_count(self):

        all_data_df=INITIALIZE_DATA().fetch_data()    
        df=LISTING_SCORE_CALCULATE().data_preprocess(all_data_df)   
        data_with_counts=LISTING_SCORE_CALCULATE().generate_counts(df)

        return data_with_counts        

    def generate_score(self,df):

        final_df=df
        final_df["score"]=""
        final_df["nameCount_score"]=""
        final_df["facetsInName_score"]=""
        final_df["descCount_score"]=""
        final_df["facetsInDesc_score"]=""
        final_df["imageCount_score"]=""
        final_df["optionalTagCount_score"]=""
        final_df["freeShipping_score"]=""
        final_df["COD_score"]=""
        final_df["returnable_score"]=""
        final_df["video_score"]=""

        for i in final_df.index:
            score=0

            if 5<final_df["name_count"][i] :
                mid=(5+25)/2
                if(final_df["name_count"][i]<=mid):
                    score+=(final_df["name_count"][i]-5)*(1)
                    final_df["nameCount_score"][i]=(final_df["name_count"][i]-5)*(1)
                else:
                    score+=10
                    final_df["nameCount_score"][i]=10			
            else:
                score+=1
                final_df["nameCount_score"][i]=1

            #For scoring on facet count in name
            if len(final_df["facets_value"][i])>0:
                score+=(final_df["facets_count_name"][i]*(25/len(final_df["facets_value"][i])))
                final_df["facetsInName_score"][i]=(final_df["facets_count_name"][i]*(25/len(final_df["facets_value"][i])))


            if 10<final_df["description_count"][i]:
                mid=(10+130)/2
                if(final_df["description_count"][i]<=mid):
                    score+=(final_df["description_count"][i]-10)*(0.166)
                    final_df["descCount_score"][i]=(final_df["description_count"][i]-10)*(0.166)
                else:	
                    score+=10
                    final_df["descCount_score"][i]=10		
            else:
                score+=0.05
                final_df["descCount_score"][i]=0.05



            if 3<=final_df["image_count"][i]:
                
                if(final_df["image_count"][i]<=10):
                    score+=(final_df["image_count"][i]-2)*(3.75)
                    final_df["imageCount_score"][i]=(final_df["image_count"][i]-2)*(3.75)
                

            final_df["returnable"]=final_df["returnable"].astype(bool)
            if final_df["returnable"][i]:
                score+=2
                final_df["returnable_score"][i]=2


            if final_df["optional_tag_count"][i]>0:
                if final_df["optional_tag_count"][i]<7:
                    score+=final_df["optional_tag_count"][i]*1.42
                    final_df["optionalTagCount_score"][i]=final_df["optional_tag_count"][i]*1.42
                else:
                    score+=10
                    final_df["optionalTagCount_score"][i]=10

            if len(final_df["facets_value"][i])>0:
                score+=(final_df["tags_count"][i]*(5/len(final_df["facets_value"][i])))
                final_df["facetsInDesc_score"][i]=(final_df["tags_count"][i]*(5/len(final_df["facets_value"][i])))
                      
            final_df["freeShipping"]=final_df["freeShipping"].astype(bool)
            if final_df["freeShipping"][i]:
                score+=2
                final_df["freeShipping_score"][i]=2

            final_df["cod"]=final_df["cod"].astype(bool)
            if final_df["cod"][i]:
                score+=1
                final_df["COD_score"][i]=1

            if df['video_count'][i]>0:
                score+=5
                final_df["video_score"][i]=5

            final_df["score"][i]=round(score,3)
              
        return final_df

    def remove_hidden(slef,df):
        
        df.drop(df[df["offerStage"] =="Hidden"].index, inplace = True)
        df.drop(df[df["offerStage"] =="Inactive"].index, inplace = True)
        df.drop(df[df["offerStage"] =="Blocked"].index, inplace = True)
        df.drop(df[df["offerStage"] =="Review"].index, inplace = True)
        df.drop(df[df["offerStage"] =="Failed"].index, inplace = True)

        return df