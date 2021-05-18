import requests
from lxml import html,etree
from flask import Flask
from flask_restful import Resource,Api

def fetch_news(domain_url):
    #domain_url = "https://www.ndtv.com/world-news"
    last_page_xpath = "//div[contains(@class,'listng_pagntn clear')]/a[contains(@class,'btnLnk arrowBtn next')]/preceding-sibling::a[position()=1]"
    page = requests.get(domain_url)
    tree = html.fromstring(page.content)
    total_pages = tree.xpath(last_page_xpath+"/text()")[0]

    print(total_pages)
    news_list = []
    
    for page in range(1,int(total_pages)+1):
        url = "{}/page-{}".format(domain_url,page)
        page = requests.get(url)
        tree = html.fromstring(page.content)
        news_header_xpath = "//h2[contains(@class,'newsHdng')]/a"
        
        latest_news_xpath = tree.xpath(news_header_xpath)
        
        for i in range(0,len(latest_news_xpath)):
            news_headline = tree.xpath(f"({news_header_xpath})[{i+1}]/text()")[0] #*
            news_link = latest_news_xpath[i].get('href') #*
            description_xpath = f"({news_header_xpath})[{i+1}]/parent::h2/following-sibling::p/text()"
            description = tree.xpath(description_xpath)[0] #*
            #print(description)
            
            img_xpath = f"({news_header_xpath})[{i+1}]/parent::h2/parent::div/preceding-sibling::div/a/img"
            img = tree.xpath(img_xpath)[0].get("src") #*
            
            news_list.append(
                {
                    "headline" : news_headline,
                    "url" : news_link,
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


app = Flask(__name__)
api = Api(app)
api.add_resource(LatestNews, "/latest-news")
api.add_resource(WorldNews, "/world-news")
api.add_resource(IndiaNews, "/india-news")

if __name__ == '__main__':
    app.run(debug=True)