from flask_restful import Resource
import pandas as pd
from flask import request
import re
import threading
import numpy as np
from sqlalchemy import create_engine
import os
from ScrapNewsAndStoreInDB import main
main()
db_url = os.environ.get("HEROKU_POSTGRESQL_SILVER_URL").replace("postgres","postgresql")
engine = create_engine(db_url, echo = False)


def fetch_news_data_from_db():
    threading.Timer(600.0, fetch_news_data_from_db).start()
    category_news_dataframe = pd.read_sql_table("category_news", engine)
    sports_news_dataframe = pd.read_sql_table("sports_news", engine)
    city_news_dataframe = pd.read_sql_table("city_news", engine)
    print("db updated")
    return category_news_dataframe, sports_news_dataframe, city_news_dataframe


def read_news_dataframe(requested_fields, requested_categories, readable_dataframe):
    total_main_news_df = readable_dataframe
    total_main_news_df["posted_date"] = total_main_news_df["posted_date"].astype(str)
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


category_news_dataframe, sports_news_dataframe, city_news_dataframe = fetch_news_data_from_db()


class LatestNews(Resource):
    
    
    def __init__(self):
        self.readable_dataframe = category_news_dataframe.copy()
        self.default_page = "latest"
        self.category_field_name = "category"
    
    
    def get(self):
        user_requested_category = request.args.get(self.category_field_name)
        user_requested_field = request.args.get("field")
        
        if user_requested_field is not None and user_requested_category is not None:
            fields_list = re.findall(r"([^(,)]+)(?!.*\()", user_requested_field)
            category_list = re.findall(r"([^(,)]+)(?!.*\()", user_requested_category)
            news_list = read_news_dataframe(
                requested_fields = fields_list,
                requested_categories = category_list,
                readable_dataframe = self.readable_dataframe
            )
        
        elif user_requested_field is not None and user_requested_category is None:
            fields_list = re.findall(r"([^(,)]+)(?!.*\()", user_requested_field)
            news_list = read_news_dataframe(
                requested_fields = fields_list,
                requested_categories = [self.default_page],
                readable_dataframe = self.readable_dataframe
            )
        
        elif user_requested_field is None and user_requested_category is not None:
            category_list = re.findall(r"([^(,)]+)(?!.*\()", user_requested_category)
            news_list = read_news_dataframe(
                requested_fields = ["category", "headline", "description", "url", "image_url", "posted_date"],
                requested_categories = category_list,
                readable_dataframe = self.readable_dataframe
            )
        
        else:
            news_list = read_news_dataframe(
                requested_fields = ["category", "headline", "description", "url", "image_url", "posted_date"],
                requested_categories = [self.default_page],
                readable_dataframe = self.readable_dataframe
            )
        
        return news_list


class SportsNews(LatestNews):
    def __init__(self):
        self.readable_dataframe = sports_news_dataframe.copy()
        self.default_page = "cricket"
        self.category_field_name = "sport"


class CityNews(LatestNews):
    def __init__(self):
        self.readable_dataframe = city_news_dataframe.copy()
        self.default_page = "cities"
        self.category_field_name = "city"