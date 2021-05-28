import requests
from lxml import html
from flask_restful import Resource
import pandas as pd
from flask import request
import re
import threading
import numpy as np
from sqlalchemy import create_engine
import time


engine = create_engine("postgresql://qmfoxldpeqyqxl:ef4a37793d151cb57a73570ec98f4f20c078de8df5fec98a2770401b20b7d578@ec2-34-202-54-225.compute-1.amazonaws.com:5432/d29c1ebursraf8", echo = False)


variable = None

class FetchNewsFromDb():
    
    
    # def __init__(self):
        
    #     self.sports_news_dataframe = pd.read_sql_table("sports_news", engine)
    #     self.city_news_dataframe = pd.read_sql_table("city_news", engine)
    
    
    def read_news_dataframe(self, requested_fields, requested_categories, readable_dataframe):
        total_main_news_df = readable_dataframe
        
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


fetch_news = FetchNewsFromDb()

class LatestNews(Resource):
    
    
    def __init__(self):
        self.readable_dataframe = pd.read_sql_table("category_news", engine)
        self.default_page = "latest"
        self.category_field_name = "category"
    
    
    def get(self):
        user_requested_category = request.args.get(self.category_field_name)
        user_requested_field = request.args.get("field")
        
        if user_requested_field is not None and user_requested_category is not None:
            fields_list = re.findall(r"([^(,)]+)(?!.*\()", user_requested_field)
            category_list = re.findall(r"([^(,)]+)(?!.*\()", user_requested_category)
            news_list = fetch_news.read_news_dataframe(
                requested_fields = fields_list,
                requested_categories = category_list,
                readable_dataframe = self.readable_dataframe
            )
        
        elif user_requested_field is not None and user_requested_category is None:
            fields_list = re.findall(r"([^(,)]+)(?!.*\()", user_requested_field)
            news_list = fetch_news.read_news_dataframe(
                requested_fields = fields_list,
                requested_categories = [self.default_page],
                readable_dataframe = self.readable_dataframe
            )
        
        elif user_requested_field is None and user_requested_category is not None:
            category_list = re.findall(r"([^(,)]+)(?!.*\()", user_requested_category)
            news_list = fetch_news.read_news_dataframe(
                requested_fields = ["category", "headline", "description", "url", "image_url"],
                requested_categories = category_list,
                readable_dataframe = self.readable_dataframe
            )
        
        else:
            news_list = fetch_news.read_news_dataframe(
                requested_fields = ["category", "headline", "description", "url", "image_url"],
                requested_categories = ["latest"]
            )
        
        return news_list

class SportsNews(LatestNews):
    def __init__(self):
        # self.readable_dataframe = fetch_news.sports_news_dataframe.copy()
        self.readable_dataframe = pd.read_sql_table("sports_news", engine)
        self.default_page = "cricket"
        self.category_field_name = "sport"

class CityNews(LatestNews):
    def __init__(self):
        # self.readable_dataframe = fetch_news.city_news_dataframe.copy()
        self.readable_dataframe = pd.read_sql_table("city_news", engine)
        self.default_page = "cities"
        self.category_field_name = "city"