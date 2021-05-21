import requests
import json
from lxml import html
from flask_restful import Resource


def fetch_news(domain_url):
    #by getting the last page in the pagination, we will come to know thw total number of pages for that category
    last_page_xpath = "//div[contains(@class,'listng_pagntn clear')]/a[contains(@class,'btnLnk arrowBtn next')]/preceding-sibling::a[position()=1]"
    page = requests.get(domain_url)
    tree = html.fromstring(page.content)
    total_pages = tree.xpath(last_page_xpath+"/text()")[0]
    
    news_list = []
    
    for page in range(1, int(total_pages) + 1):
        url = "{}/page-{}".format(domain_url,page)
        page = requests.get(url)
        tree = html.fromstring(page.content)
        news_header_xpath = "//h2[contains(@class,'newsHdng')]/a"
        
        latest_news_xpath = tree.xpath(news_header_xpath)
        
        for i in range(0,len(latest_news_xpath)):
            news_headline = tree.xpath(f"({news_header_xpath})[{i+1}]/text()")[0] #*headline
            news_link = latest_news_xpath[i].get('href') #*url
            description_xpath = f"({news_header_xpath})[{i+1}]/parent::h2/following-sibling::p/text()"
            description = tree.xpath(description_xpath)[0] #*description
            img_xpath = f"({news_header_xpath})[{i+1}]/parent::h2/parent::div/preceding-sibling::div/a/img"
            img = tree.xpath(img_xpath)[0].get("src") #*image_url
            
            news_list.append(
                {
                    "headline" : news_headline,
                    "url" : news_link,
                    "description" : description,
                    "image_url" : img
                }
            )
    return news_list


def fetch_sports_news(url):
    
    page = requests.get(url)
    tree = html.fromstring(page.content)
    headline_xpath = "//li[contains(@class,'lst-pg-a-li')]/div/div/a"
    headlines_list = tree.xpath(headline_xpath + "/text()")
    
    news_list = []
    
    for headline in range(1, int(len(headlines_list)) + 1):
        news_headline = headlines_list[int(headline) - 1]
        news_url = tree.xpath(f"({headline_xpath})[{headline}]")[0].get("href")
        description_xpath = f"({headline_xpath})[{headline}]/following-sibling::p/text()"
        description = tree.xpath(description_xpath)[0]
        image_xpath = f"({headline_xpath})[{headline}]/parent::div/preceding-sibling::a/div/img/@data-a-dynamic-image"
        
        img = tree.xpath(image_xpath)#[0]#.get("src") #*image_url
        
        news_list.append(
                {
                    "headline" : news_headline,
                    "url" : news_url,
                    "description" : description,
                    "image_url" : img
                }
            )
    return news_list


class LatestNews(Resource):
    def get(self):
        news_list = fetch_news(domain_url = "https://www.ndtv.com/latest")
        return {"news_list" : news_list}

class WorldNews(Resource):
    def get(self):
        news_list = fetch_news(domain_url = "https://www.ndtv.com/world-news")
        return {"news_list" : news_list}

class IndiaNews(Resource):
    def get(self):
        news_list = fetch_news(domain_url = "https://www.ndtv.com/india")
        return {"news_list" : news_list}

class ScienceNews(Resource):
    def get(self):
        news_list = fetch_news(domain_url = "https://www.ndtv.com/science")
        return {"news_list" : news_list}

class BusinessNews(Resource):
    def get(self):
        news_list = fetch_news(domain_url = "https://www.ndtv.com/business/latest")
        return {"news_list" : news_list}

class EntertainmentNews(Resource):
    def get(self):
        news_list = fetch_news(domain_url = "https://www.ndtv.com/entertainment/latest")
        return {"news_list" : news_list}

class GeneralNews(Resource):
    def __init__(self,url):
        self.url = url
    
    def get(self):
        news_list = fetch_news(domain_url = self.url)
        return {"news_list" : news_list}

class SportsNews(Resource):
    def get(self):
        news_list = fetch_sports_news(url = "https://sports.ndtv.com/football/news")
        return {"news_list" : news_list}