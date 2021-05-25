from flask import Flask
from flask_restful import Api
from NDTV import LatestNews



cities = ["agra","ahmedabad","allahabad","amritsar","aurangabad","bangalore","bhopal","bhubaneshwar","chandigarh","chennai","delhi","ghaziabad","goa","gurgaon","guwahati"]

app = Flask(__name__)
api = Api(app)
api.add_resource(LatestNews, "/category")

if __name__ == '__main__':
    app.run(debug=True)
