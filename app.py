from flask import Flask
from flask_restful import Api
from NDTV import LatestNews, WorldNews, IndiaNews, ScienceNews, BusinessNews,  EntertainmentNews

app = Flask(__name__)
api = Api(app)
api.add_resource(LatestNews, "/latest-news")
api.add_resource(WorldNews, "/world-news")
api.add_resource(IndiaNews, "/india-news")
api.add_resource(ScienceNews, "/science-news")
api.add_resource(BusinessNews, "/business-news")
api.add_resource(EntertainmentNews, "/entertainment-news")

if __name__ == '__main__':
    app.run(debug=True)
