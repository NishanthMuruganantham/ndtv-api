from flask_restful import Resource
import pandas as pd
from flask import request
import re
import threading
import numpy as np
import os
from pymongo import MongoClient


#fetching db url from entertainmental variables
db_url = os.environ.get('MONGO_DB_URL')
client = MongoClient(db_url)
db_name = client[os.environ.get('DB_NAME')]
print("db connection established")

general_news_dataframe = None
sports_news_dataframe = None
city_news_dataframe = None

with open(r"README.md", "r") as f:
    readme_content = f.read()
    print("readme file content has been fetched")


def fetch_news_data_from_db():
    
    """
    [fetch_news_data_from_db]
        It will fetch the news stored in the database and store it in a dataframe for convenient and faster accessing
    """
    
    threading.Timer(600.0, fetch_news_data_from_db).start()             #threaded to run every 10 minutes to keep the news dataframe updated
    global general_news_dataframe
    general_news_dataframe = pd.DataFrame(list(db_name["general_news"].find()))
    print("general news dataframe has been updated")
    
    global sports_news_dataframe
    sports_news_dataframe = pd.DataFrame(list(db_name["sports_news"].find()))
    print("sports news dataframe has been updated")
    
    global city_news_dataframe
    city_news_dataframe = pd.DataFrame(list(db_name["city_news"].find()))
    print("city news dataframe has been updated")


def read_news_dataframe(requested_fields, requested_categories, readable_dataframe):
    
    """
    [read_news_dataframe]
        Once, a request is received, this function wil be triggered from the respective Resource class.
        This will read the news dataframe and return the JSON object which will contain the list of news dictionaries.
        
    Args:
        requested_fields ([type]): [The news field requested for that request]
        requested_categories ([type]): [The requested news category]
        readable_dataframe ([type]): [The dataframe for the respective News category]
    
    Returns:
        [dict]: [JSON containing a list of news dictionaries]
    """
    
    total_main_news_df = readable_dataframe
    total_main_news_df["posted_date"] = pd.to_datetime(total_main_news_df["posted_date"], format = "%Y-%m-%d")
    total_main_news_df["posted_date"] = total_main_news_df["posted_date"].dt.strftime("%d-%m-%Y")
    total_main_news_df["posted_date"] = total_main_news_df["posted_date"].astype(str)   #converting data column to string
    output_category_list = []
    
    for category in requested_categories:
        category_wise_df = total_main_news_df[total_main_news_df["category"] == category]
        category_wise_df_with_requested_fields = category_wise_df[requested_fields]
        category_wise_df_with_requested_fields = (
            category_wise_df_with_requested_fields.replace({np.nan: None})
        )
        
        news_list = []
        for index, row in category_wise_df_with_requested_fields.iterrows():
            response_dict = (
                {i: row[i] for i in category_wise_df_with_requested_fields.columns}
            )
            news_list.append(response_dict)
        
        category_dictionary = {
            "category": category,
            "total_results": len(category_wise_df_with_requested_fields),
            "articles": news_list,
        }
        
        output_category_list.append(category_dictionary)
    
    return {"news": output_category_list}


fetch_news_data_from_db()


class GeneralNews(Resource):
    
    def __init__(self):
        self.readable_dataframe = general_news_dataframe.copy()
        self.default_page = "latest"            #represents the default news category if user is not specifying any 
        self.category_field_name = "category"   #defined the category field name for each type of news - E.g : ?category=values(latest,india)
    
    
    def get(self):
        user_requested_category = request.args.get(self.category_field_name)    #fetching the requested category from incoming request
        user_requested_field = request.args.get("field")                        #fetching the fields requested by user from incoming request
        
        if user_requested_field is not None and user_requested_category is not None:    #if user specifying both category and field
            fields_list = re.findall(r"([^(,)]+)(?!.*\()", user_requested_field)
            category_list = re.findall(r"([^(,)]+)(?!.*\()", user_requested_category)
            news_list = read_news_dataframe(
                requested_fields = fields_list,
                requested_categories = category_list,
                readable_dataframe = self.readable_dataframe
            )
        
        elif user_requested_field is not None and user_requested_category is None:      #if user is is not specifying any news category, but requests field. 
            fields_list = re.findall(r"([^(,)]+)(?!.*\()", user_requested_field)
            news_list = read_news_dataframe(
                requested_fields = fields_list,
                requested_categories = [self.default_page],
                readable_dataframe = self.readable_dataframe
            )
        
        elif user_requested_field is None and user_requested_category is not None:      #if user is not specifying any fields but specifying news category
            category_list = re.findall(r"([^(,)]+)(?!.*\()", user_requested_category)
            news_list = read_news_dataframe(
                requested_fields = ["category", "headline", "description", "url", "image_url", "posted_date"],
                requested_categories = category_list,
                readable_dataframe = self.readable_dataframe
            )
        
        else:                                       #if user is not specifying any, defaultly default category and all fields will be returned
            news_list = read_news_dataframe(
                requested_fields = ["category", "headline", "description", "url", "image_url", "posted_date"],
                requested_categories = [self.default_page],
                readable_dataframe = self.readable_dataframe
            )
        
        return news_list


class SportsNews(GeneralNews):  #inherited from general news
    def __init__(self):
        self.readable_dataframe = sports_news_dataframe.copy()
        self.default_page = "cricket"
        self.category_field_name = "sport"


class CityNews(GeneralNews):    #inherited from general news
    def __init__(self):
        self.readable_dataframe = city_news_dataframe.copy()
        self.default_page = "cities"
        self.category_field_name = "city"