from flask import Flask
from flask_restful import Api
from NDTV import LatestNews, SportsNews, CityNews


app = Flask(__name__)
api = Api(app)
api.add_resource(LatestNews, "/categories")
api.add_resource(SportsNews, "/sports")
api.add_resource(CityNews, "/cities")

if __name__ == '__main__':
    app.run(debug=False)
