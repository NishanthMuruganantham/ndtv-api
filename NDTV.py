import requests
import json
from lxml import html
from flask_restful import Resource
import pandas as pd
from flask import Flask, request
import re



def fetch_news(news_page_url,fields_list = ["headline","url","description","image_url"]):
    #by getting the last page in the pagination, we will come to know thw total number of pages for that category
    last_page_xpath = "//div[contains(@class,'listng_pagntn clear')]/a[contains(@class,'btnLnk arrowBtn next')]/preceding-sibling::a[position()=1]"
    page = requests.get(news_page_url)
    tree = html.fromstring(page.content)
    total_pages = tree.xpath(last_page_xpath+"/text()")[0]
    
    news_list = []
    
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
            
            default_news_dict = {
                    "headline" : news_headline,
                    "url" : news_url,
                    "description" : description,
                    "image_url" : img_url
                }
            
            requested_news_dict = {key: default_news_dict[key] for key in default_news_dict.keys() & set(fields_list)}
            news_list.append(
                requested_news_dict
            )
    
    return news_list


class LatestNews(Resource):
    def get(self):
        user_requested_field = request.args.get("field")
        if user_requested_field is not None:
            fields_list = re.findall(r'([^(,)]+)(?!.*\()', user_requested_field)
            news_list = fetch_news(news_page_url = "https://www.ndtv.com/latest",fields_list = fields_list)
        else:
            news_list = fetch_news(news_page_url = "https://www.ndtv.com/latest")
        return {"news_list" : news_list}
