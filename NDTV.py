import requests
from lxml import html
from flask_restful import Resource
import pandas as pd
from flask import request
import re
import threading
import numpy as np
from sqlalchemy import create_engine

main_news_csv = r"main_news.csv"

engine = create_engine("postgresql://qmfoxldpeqyqxl:ef4a37793d151cb57a73570ec98f4f20c078de8df5fec98a2770401b20b7d578@ec2-34-202-54-225.compute-1.amazonaws.com:5432/d29c1ebursraf8", echo = False)


variable = None

class CategoryNews():
    
    
    def __init__(self):
        self.main_news_dataframe = pd.DataFrame(
            columns=["category", "headline", "description", "url", "image_url"]
        )
        self.available_categories = {
            # "latest": "https://www.ndtv.com/latest",
            "india": "https://www.ndtv.com/india",
            "science": "https://www.ndtv.com/science",
            "business": "https://www.ndtv.com/business/latest",
            # "entertainment": "https://www.ndtv.com/entertainment/latest",
            # "offbeat" : "https://www.ndtv.com/offbeat",
        }
        self.readable_dataframe = pd.read_sql_table("sample", engine)
    
    
    def scrap_page_and_fetch_news_data(self, category, news_page_url):
        news_df = pd.DataFrame(
            columns=["category", "headline", "description", "url", "image_url"]
        )
        
        last_page_xpath = "//div[contains(@class,'listng_pagntn clear')]/a[contains(@class,'btnLnk arrowBtn next')]/preceding-sibling::a[position()=1]"
        page = requests.get(news_page_url)
        tree = html.fromstring(page.content)
        total_pages = tree.xpath(last_page_xpath + "/text()")[0]
        
        headline_list = []
        description_list = []
        image_url_list = []
        url_list = []
        
        for page in range(1, int(total_pages) + 1):
            
            page_url = f"{news_page_url}/page-{page}"
            page = requests.get(page_url)
            tree = html.fromstring(page.content)
            news_header_xpath = "//h2[contains(@class,'newsHdng')]/a"
            headline_elements = tree.xpath(news_header_xpath)
            
            for i in range(1, int(len(headline_elements)) + 1):
                try:
                    news_headline = tree.xpath(f"({news_header_xpath})[{i}]/text()")[0]  # *headline
                except IndexError:
                    news_headline = None
                
                try:
                    news_url = headline_elements[i - 1].get("href")  # *url
                except:
                    news_url = None
                
                description_xpath = f"({news_header_xpath})[{i}]/parent::h2/following-sibling::p/text()"
                try:
                    description = tree.xpath(description_xpath)[0]  # *description
                except IndexError:
                    description = None
                
                img_xpath = f"({news_header_xpath})[{i}]/parent::h2/parent::div/preceding-sibling::div/a/img"
                try:
                    img_url = tree.xpath(img_xpath)[0].get("src")  # *image_url
                except IndexError:
                    img_url = None
                
                headline_list.append(news_headline)
                description_list.append(description)
                image_url_list.append(img_url)
                url_list.append(news_url)
        
        news_df["headline"] = headline_list
        news_df["description"] = description_list
        news_df["url"] = url_list
        news_df["image_url"] = image_url_list
        news_df = news_df.assign(category = category)
        
        return news_df
    
    
    def store_news_in_dataframe(self):
        threading.Timer(300.0, self.store_news_in_dataframe).start()
        global variable
        if variable is None:
            
            variable = 1
            print("changed")
            pass
        else:    
            print("second run")
            L = []
            for category in self.available_categories:
                df = self.scrap_page_and_fetch_news_data(
                    category = category, news_page_url = self.available_categories[category]
                )
                L.append(df)
            
            self.main_news_dataframe = pd.concat(L, ignore_index = True)
            self.main_news_dataframe.to_csv(main_news_csv, sep=",", index = False)
            self.main_news_dataframe.to_sql('sample', con = engine, if_exists='replace')
            self.readable_dataframe = pd.read_sql_table("sample", engine)
            print("reassigned")
    
    def read_news_dataframe(self, requested_fields, requested_categories):
        #total_main_news_df = self.main_news_dataframe.copy()
        #total_main_news_df = pd.read_csv(main_news_csv)
        total_main_news_df = self.readable_dataframe.copy()
        
        output_category_list = []
        for category in requested_categories:
            category_wise_df = total_main_news_df[total_main_news_df["category"] == category]
            category_wise_df_with_requested_fields = category_wise_df[requested_fields]
            category_wise_df_with_requested_fields = (
                category_wise_df_with_requested_fields.replace({np.nan: None})
            )
            
            news_list = []
            for index, row in category_wise_df_with_requested_fields.iterrows():
                response_dict = {"count": "d"}
                response_dict.update(
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


def fetch_sports_news():

    page = requests.get("sports.ndtv.com/cricket/news")
    tree = html.fromstring(page.content)
    news_header_xpath = "//li[contains(@class,'lst-pg-a-li')]/div/div/a"
    headline_elements = tree.xpath(news_header_xpath)

    headline_list = []
    description_list = []
    image_url_list = []
    url_list = []

    for i in range(1, int(len(headline_elements)) + 1):
        try:
            news_headline = tree.xpath(f"({news_header_xpath})[{i}]/text()")[0]  # *headline
            print(news_headline)
        except IndexError:
            news_headline = None
        
        try:
            news_url = headline_elements[i - 1].get("href")  # *url
        except:
            news_url = None
        
        description_xpath = f"({news_header_xpath})[{i}]/following-sibling::p/text()"
        try:
            description = tree.xpath(description_xpath)[0]  # *description
        except IndexError:
            description = None
        
        img_xpath = f"({news_header_xpath})[{i}]/parent::div/preceding-sibling::a/div/img"
        try:
            img_url = tree.xpath(img_xpath)[0].get("src")  # *image_url
        except IndexError:
            img_url = None
        
        headline_list.append(news_headline)
        description_list.append(description)
        image_url_list.append(img_url)
        url_list.append(news_url)
    


category_news = CategoryNews()

category_news.store_news_in_dataframe()
#read_dataframe()


class LatestNews(Resource):
    def get(self):
        user_requested_category = request.args.get("category")
        user_requested_field = request.args.get("field")
        
        if user_requested_field is not None and user_requested_category is not None:
            fields_list = re.findall(r"([^(,)]+)(?!.*\()", user_requested_field)
            category_list = re.findall(r"([^(,)]+)(?!.*\()", user_requested_category)
            news_list = category_news.read_news_dataframe(
                requested_fields = fields_list, requested_categories = category_list
            )
        
        elif user_requested_field is not None and user_requested_category is None:
            fields_list = re.findall(r"([^(,)]+)(?!.*\()", user_requested_field)
            news_list = category_news.read_news_dataframe(
                requested_fields = fields_list,
                requested_categories = ["latest"]
            )
        
        elif user_requested_field is None and user_requested_category is not None:
            category_list = re.findall(r"([^(,)]+)(?!.*\()", user_requested_category)
            news_list = category_news.read_news_dataframe(
                requested_fields = ["category", "headline", "description", "url", "image_url"],
                requested_categories = category_list
            )
        
        else:
            news_list = category_news.read_news_dataframe(
                requested_fields = ["category", "headline", "description", "url", "image_url"],
                requested_categories = ["latest"]
            )
        
        return news_list
