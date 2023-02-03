"""
[PROCESS]
1) Scrap NDTV website Data using requests and LXML (ScrapNewsAndStoreInDb.py)
2) Store the data in a database using SQLAlchemy   (ScrapNewsAndStoreInDb.py) 
3) Fetch the news from Database and feed to the dataframe using SQLAlchemy and Pandas (NDTV.py)
4) Once a request is received, query the respective dataframe accoring to the user request using Pandas and Flask (NDTV.py)
5) Return the JSON response

[STEPS TO RUN THE APP.PY]
STEP - 1: install the required dependencies using : pip install -r requirements.txt
STEP - 2: Create a db of anykind[postgres, sqlite, etc.,] and specify that URL as environment variable
STEP - 3: Run the ScrapNewsAndStoreInDb.py file (specify the environment variable). Schedule the script according to the need to keep the Database updated
STEP - 4: Run the app.py file
"""

from flask import Flask
from flask_restful import Api
from NDTV import GeneralNews, SportsNews, CityNews, readme_content


app = Flask(__name__)
@app.route("/")
def index():
    return readme_content


api = Api(app)
api.add_resource(GeneralNews, "/general")
api.add_resource(SportsNews, "/sports")
api.add_resource(CityNews, "/cities")


if __name__ == '__main__':
    app.run(debug = False)