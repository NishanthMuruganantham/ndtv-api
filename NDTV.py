import requests
from lxml import html
from flask_restful import Resource
import pandas as pd
from flask import request
import re
import threading
import numpy as np

main_news_csv = r"main_news.csv"


def fetch_main_news_data(category,news_page_url):
    
    news_df = pd.DataFrame(columns = ["category","headline","description","url","image_url"])
    
    #news_page_url = "https://www.ndtv.com/latest"
    last_page_xpath = "//div[contains(@class,'listng_pagntn clear')]/a[contains(@class,'btnLnk arrowBtn next')]/preceding-sibling::a[position()=1]"
    page = requests.get(news_page_url)
    tree = html.fromstring(page.content)
    total_pages = tree.xpath(last_page_xpath+"/text()")[0]
    
    news_list = []
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
        
        for i in range(1,int(len(headline_elements)) + 1):
            
            news_headline = tree.xpath(f"({news_header_xpath})[{i}]/text()")[0] #*headline
            news_url = headline_elements[i-1].get('href') #*url
            description_xpath = f"({news_header_xpath})[{i}]/parent::h2/following-sibling::p/text()"
            description = tree.xpath(description_xpath)[0] #*description
            img_xpath = f"({news_header_xpath})[{i}]/parent::h2/parent::div/preceding-sibling::div/a/img"
            img_url = tree.xpath(img_xpath)[0].get("src") #*image_url
            
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

main_categories = {
    "latest" : "https://www.ndtv.com/latest",
    # "india" : "https://www.ndtv.com/india",
    # "science" : "https://www.ndtv.com/science",
    # "business" : "https://www.ndtv.com/business/latest",
    # "entertainment" : "https://www.ndtv.com/entertainment/latest",
}


def store_news_in_csv():
    threading.Timer(120.0, store_news_in_csv).start()
    L = []
    for category in main_categories:
        df = fetch_main_news_data(category = category, news_page_url = main_categories[category])
        L.append(df)
    
    news_df = pd.concat(L, ignore_index=True)
    print(news_df)
    news_df.to_csv(main_news_csv, sep = ',', index = False)



def read_excel(requested_fields = ["category","headline","description","url","image_url"]):
    news = pd.read_csv(main_news_csv)
    news = news[requested_fields]
    news = news.replace({np.nan: None})
    news_list = []
    for index, row in news.iterrows():
        response_dict = {i:row[i] for i in news.columns}
        news_list.append(response_dict)
    return {"news_list": news_list}

#store_news_in_csv()

class LatestNews(Resource):
    def get(self):
        user_requested_field = request.args.get("field")
        if user_requested_field is not None:
            fields_list = re.findall(r'([^(,)]+)(?!.*\()', user_requested_field)
            news_list = read_excel(requested_fields = fields_list)
        else:
            news_list = read_excel()
        return news_list
read_excel()
