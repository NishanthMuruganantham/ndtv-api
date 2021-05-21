from flask import Flask
from flask_restful import Api
from NDTV import LatestNews, WorldNews, IndiaNews, ScienceNews, BusinessNews,  EntertainmentNews, GeneralNews, SportsNews

cities = ["agra","ahmedabad","allahabad","amritsar","aurangabad","bangalore","bhopal","bhubaneshwar","chandigarh","chennai","delhi","ghaziabad","goa","gurgaon","guwahati"]

app = Flask(__name__)
api = Api(app)
api.add_resource(LatestNews, "/latest-news")
api.add_resource(WorldNews, "/world-news")
api.add_resource(IndiaNews, "/india-news")
api.add_resource(ScienceNews, "/science-news")
api.add_resource(BusinessNews, "/business-news")
api.add_resource(EntertainmentNews, "/entertainment-news")
api.add_resource(GeneralNews,"/general-news",resource_class_kwargs={'url': "https://www.ndtv.com/world-news"})
api.add_resource(SportsNews, "/sports-news")

# for city in cities:
#     api.add_resource(GeneralNews,f"/{city}-news",resource_class_kwargs={'url': f"https://www.ndtv.com/{city}-news"})

if __name__ == '__main__':
    app.run(debug=True)
