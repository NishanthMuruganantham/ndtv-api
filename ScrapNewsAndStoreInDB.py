from sqlalchemy import create_engine
from lxml import html
import pandas as pd
import requests
from dateutil.parser import parse
import os


#fetching db url from entertainmental variables
db_url = os.environ.get("HEROKU_POSTGRESQL_SILVER_URL").replace("postgres","postgresql")
engine = create_engine(db_url, echo = False)
print("db connection established")


#This is the class to scrap the Categorywise news present in the NDTV site and store it to a database.
#This class can also be inherited to SportsNews class and CityNews class.
class GeneralNews():
    
    
    def __init__(self):
        self.main_news_dataframe = pd.DataFrame(
            columns = ["category", "headline", "description", "url", "image_url", "posted_date"]
        )
        self.available_categories = {
            "latest"    : "https://www.ndtv.com/latest",
            "india"     : "https://www.ndtv.com/india",
            "world"     : "https://www.ndtv.com/world-news",
            "science"   : "https://www.ndtv.com/science",
            "business"  : "https://www.ndtv.com/business/latest",
            "entertainment": "https://www.ndtv.com/entertainment/latest",
            "offbeat"   : "https://www.ndtv.com/offbeat",
        }
    
    #this function will scrap the news using LXML's HTML by xpath
    def scrap_page_and_fetch_news_data(self, category, news_page_url):
        news_df = pd.DataFrame(
            columns = ["category", "headline", "description", "url", "image_url", "posted_date"]
        )
        
        #finding the last entry in the pagination to find the total pages present for the particoular category
        last_page_xpath = "//div[contains(@class,'listng_pagntn clear')]/a[contains(@class,'btnLnk arrowBtn next')]/preceding-sibling::a[position()=1]"
        page = requests.get(news_page_url)
        tree = html.fromstring(page.content)
        try:
            total_pages = tree.xpath(last_page_xpath + "/text()")[0]
        except:
            total_pages = 1
        
        headline_list = []
        description_list = []
        image_url_list = []
        url_list = []
        posted_date_list = []
        
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
                
                posted_date_xpath = f"({news_header_xpath})[{i}]/parent::h2/following-sibling::span/text()"
                try:
                    posted_date_span = tree.xpath(posted_date_xpath)  # *posted date
                    posted_date = None
                    for text in posted_date_span:
                        try:
                            posted_date = parse(text, fuzzy = True).date()
                        except:
                            pass
                except IndexError:
                    posted_date = None
                
                headline_list.append(news_headline)
                description_list.append(description)
                image_url_list.append(img_url)
                url_list.append(news_url)
                posted_date_list.append(posted_date)
        
        news_df["headline"] = headline_list
        news_df["description"] = description_list
        news_df["url"] = url_list
        news_df["image_url"] = image_url_list
        news_df["posted_date"] = posted_date_list
        news_df = news_df.assign(category = category)
        
        return news_df
    
    #this function will store the scrapped news data in a Database which will later feed those news to the featured API
    def store_news_in_database(self, table_name):
        L = []
        for category in self.available_categories:
            df = self.scrap_page_and_fetch_news_data(
                category = category, news_page_url = self.available_categories[category]
            )
            L.append(df)
        
        self.main_news_dataframe = pd.concat(L, ignore_index = True)
        self.main_news_dataframe.to_sql(table_name, con = engine, if_exists='replace')



#This is the class to scrap the Sports news present in https://sports.ndtv.com
class SportsNews(GeneralNews):
    
    def __init__(self):
        self.main_news_dataframe = pd.DataFrame(
            columns=["category", "headline", "description", "url", "image_url", "posted_date"]
        )
        self.available_categories = {
            "cricket"   : "https://sports.ndtv.com/cricket/news",
            "football"  : "https://sports.ndtv.com/football/news",
            "tennis"    : "https://sports.ndtv.com/tennis/news",
            "formula-1" : "https://sports.ndtv.com/formula-1/news",
            "hockey"    : "https://sports.ndtv.com/hockey/news",
            "golf"      : "https://sports.ndtv.com/golf/news",
            "badminton" : "https://sports.ndtv.com/badminton/news",
            "chess"     : "https://sports.ndtv.com/chess/news",
            "kabaddi"   : "https://sports.ndtv.com/kabaddi/news",
            "wrestling" : "https://sports.ndtv.com/wrestling/news",
            "nba"       : "https://sports.ndtv.com/nba/news",
            "boxing"    : "https://sports.ndtv.com/boxing/news",
        }
    
    
    def scrap_page_and_fetch_news_data(self, category, news_page_url):
        news_df = pd.DataFrame(
            columns=["category", "headline", "description", "url", "image_url", "posted_date"]
        )
        
        page = requests.get(news_page_url)
        tree = html.fromstring(page.content)
        news_header_xpath = "//li[contains(@class,'lst-pg-a-li')]/div/div/a"
        headline_elements = tree.xpath(news_header_xpath)
        
        headline_list = []
        description_list = []
        image_url_list = []
        url_list = []
        posted_date_list = []
        
        for i in range(1, int(len(headline_elements)) + 1):
            try:
                news_headline = tree.xpath(f"({news_header_xpath})[{i}]/text()")[0]  # *headline
            except IndexError:
                news_headline = None
            
            try:
                news_url = headline_elements[i - 1].get("href")  # *url
                news_url = "https://sports.ndtv.com/" + news_url
            except:
                news_url = None
            
            description_xpath = f"({news_header_xpath})[{i}]/following-sibling::p/text()"
            try:
                description = tree.xpath(description_xpath)[0]  # *description
            except IndexError:
                description = None
            
            img_xpath = f"({news_header_xpath})[{i}]/parent::div/preceding-sibling::a/div/img"
            try:
                img_url = tree.xpath(img_xpath)[0].get("data-srcset")  # *image_url
            except IndexError:
                img_url = None
            
            posted_date_xpath = f"({news_header_xpath})[{i}]/preceding-sibling::nav/ul/li[1]/span/text()"
            try:
                posted_date = tree.xpath(posted_date_xpath)[0]
                posted_date = parse(posted_date, fuzzy = True).date()
            except IndexError:
                posted_date = None
            
            headline_list.append(news_headline)
            description_list.append(description)
            image_url_list.append(img_url)
            url_list.append(news_url)
            posted_date_list.append(posted_date)
        
        news_df["headline"] = headline_list
        news_df["description"] = description_list
        news_df["url"] = url_list
        news_df["image_url"] = image_url_list
        news_df["posted_date"] = posted_date_list
        news_df = news_df.assign(category = category)
        
        return news_df



#This is the class to scrap the City wise news
class CityNews(GeneralNews):
    
    
    def __init__(self):
        self.main_news_dataframe = pd.DataFrame(
            columns = ["category", "headline", "description", "url", "image_url", "posted_date"]
        )
        
        cities = [
                    "agra",
                    "ahmedabad",
                    "allahabad",
                    "amritsar",
                    "aurangabad",
                    "bangalore",
                    "bhopal",
                    "bhubaneshwar",
                    "chandigarh",
                    "chennai",
                    "delhi",
                    "ghaziabad",
                    "goa",
                    "gurgaon",
                    "guwahati",
                    "hyderabad",
                    "jaipur",
                    "jammu",
                    "kanpur",
                    "kolkata",
                    "lucknow",
                    "ludhiana",
                    "meerut",
                    "mumbai",
                    "muzaffarnagar",
                    "muzaffarpur",
                    "nagpur",
                    "noida",
                    "others",
                    "patna",
                    "pune",
                    "srinagar",
                    "surat",
                    "thiruvananthapuram"
                ]
        
        self.available_categories = {
            "cities"        : "https://www.ndtv.com/cities",
        }
        
        self.available_categories.update({city : f"https://www.ndtv.com/{city}-news" for city in cities})


if __name__ == '__main__':
    
    print("scrapping started")
    
    general_news = GeneralNews()
    general_news.store_news_in_database(table_name = "general_news")
    print("scrapped general news and successfully stored in DB")
    
    sports_news = SportsNews()
    sports_news.store_news_in_database(table_name = "sports_news")   #inherited from GeneralNews
    print("scrapped sports news and successfully stored in DB")
    
    city_news = CityNews()
    city_news.store_news_in_database(table_name = "city_news")     #inherited from GeneralNews
    print("scrapped city news and successfully stored in DB")
    
    print("scrapping completed")