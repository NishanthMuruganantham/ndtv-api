# NDTV News API

This API will scrap the news content present in the NDTV website will provide the data in a JSON format.

URL : https://ndtvnews-api.herokuapp.com
___________________________________________________

**Available Endpoints:-**
===================================================
Below are the endpoints available in this API.


S.No| Categories | Endpoints
---------|----------|---------
 1  | Main News     | /categories
 2  | Sports News   | /sports
 3  | City News     | /cities

___________________________________________________

**Field Names:-**
===================================================




| S.No | Content                | Field Name  |
| ---- | ---------------------- | ----------- |
| 1    | News Classification    | category    |
| 2    | News Headline          | headline    |
| 3    | News Short Description | description |
| 4    | Actual News Url        | url         |
| 5    | News Image             | image_url   |
| 6    | Posted Date            | posted_date |

**AVAILABLE ENDPOINTS :-**

This API will scrap the data from the NDTV website and store the scrapped data in a Database (for every 10 minutes). The app will continuously be feeded using a Dataframe with the Data present in the database
