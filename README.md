# NDTV News API

<p>This API will scrap the news content present in the NDTV website will provide the data in a JSON format.</p>

URL : https://ndtvnews-api.herokuapp.com

<hr>

<h2>Available Endpoints</h2>

Below are the endpoints available in this API.

| S. No | Categories  | Endpoints   |
| ----- | ----------- | ----------- |
| 1     | General News| /general    |
| 2     | Sports News | /sports     |
| 3     | City News   | /cities     |

<hr>

<h2>Field Names</h2>

| S. No | Field Name  | Content                |
| ----- | ----------- | ---------------------- |
| 1     | category    | News Classification    |
| 2     | headline    | News Headline          |
| 3     | description | News Short Description |
| 4     | url         | Actual News Url        |
| 5     | image_url   | News Image             |
| 6     | posted_date | Posted Date            |

<hr>

<h2>Usage</h2>

<p>Please find the instructions for using the respective endpoints.</p>

<h3>For https://ndtvnews-api.herokuapp.com/general :-</h3>

<p>This endpoint will give you the news for the below mentioned categories.</p>

> <p>
> <ol>
> <li>latest      //latest news available in NDTV site for all categories</li>
> <li>india  //Indian National News</li>
> <li>world</li>
> <li>science</li>
> <li>business</li>
> <li>entertainment</li>
> <li>offbeat</li>
> </ol>
> </p>

<br>
<p>This endpoint has the below two keys which you can use to get the more specific News with the content you wish to get.</p>

Key | Name |Example
---------|----------|---------
 category | news category you wish to get | https://ndtvnews-api.herokuapp.com/general?category=values(latest,india,world)
 field | field content | https://ndtvnews-api.herokuapp.com/general?field=values(headline,description,url)
<br>

<h4>GET REQUEST :-</h4>
<br>

```
https://ndtvnews-api.herokuapp.com/general?category=values(latest)&field=values(headline,description,url)
```

<h4>OUTPUT :-</h4>
<br>

```JSON
{
    "news": [
        {
            "category": "latest",
            "total_results": 2,
            "articles": [
                {
                    "headline": "25,000 Tonnes Of Oxygen Delivered Across India So Far: Railways",
                    "description": "The railways 'Oxygen Express' trains have crossed the milestone of delivering 25,000 tonnes of liquid medical oxygen across 39 cities in 15 states/UTs amid the COVID-19 outbreak, the national transporter said on Saturday.",
                    "url": "https://www.ndtv.com/india-news/25-000-tonnes-of-oxygen-delivered-across-india-so-far-railways-2457156",
                },
                {
                    "headline": "Monsoon Arrives In Maharashtra; Conditions Favourable For Advancement: Weather Office",
                    "description": "The southwest monsoon arrived in Maharashtra on Saturday, bringing showers in some coastal parts of the state, an India Meteorological Department (IMD) official said.",
                    "url": "https://www.ndtv.com/india-news/monsoon-arrives-in-maharashtra-conditions-favourable-for-advancement-weather-office-2457092",
                }
            ]
        },
        {
            "category": "india",
            "total_results": 1,
            "articles": [
                {
                    "headline": "Haryana Farmers March On Police Station In Showdown Over Spat With MLA",
                    "description": "Hundreds of farmers marched on the police station in Haryana's Tohana Saturday to court arrest in protest of the arrest of three of their colleagues, and raids on their camps and homes, after a spat with local MLA Devendra Babli of the JJP",
                    "url": "https://www.ndtv.com/india-news/farmers-protest-tohana-haryana-farmers-march-on-police-station-in-showdown-over-spat-with-mla-2457164",
                }
            ]
        },
        {
            "category": "world",
            "total_results": 2,
            "articles": [
                {
                    "headline": "Turkish Drone Strike Kills 3 Civilians In Iraq Refugee Camp",
                    "description": "Three civilians were killed Saturday in a Turkish drone attack on a refugee camp in northern Iraq in an area Turkish President recently threatened to \"clean up\", a Kurdish lawmaker said.",
                    "url": "https://www.ndtv.com/world-news/turkish-drone-strike-kills-3-civilians-in-iraq-refugee-camp-2457161",
                },
                {
                    "headline": "Global Terror Funding Watchdog Retains Pak On \"Enhanced Follow-Up\" List",
                    "description": "The Asia Pacific Group on Money Laundering has retained Pakistan on \"enhanced follow-up\" status for outstanding requirements.",
                    "url": "https://www.ndtv.com/world-news/global-terror-funding-watchdog-fatf-retains-pakistan-on-enhanced-follow-up-list-2457134",
                }
            ]
        }
    ]
}

```
<br>
<p>
Hence, it will give you a dictionary with a key called news and the value containing a list of dictionaries (this dictionary will hold the requested news category, total_results and the news data list) for the requested categories.
</p>
<p>
If you are not specifying any keys and just simply hit the endpoint, it will give you the news from latest category with all the available fields (category, headline, description, url, image_url,  posted_date).
</p>
<hr>
<h3>For https://ndtvnews-api.herokuapp.com/cities :-</h3>

<p>This will give you the news related to the below mentioned cities.</p>

> <p>
> <ol>
> <li>agra</li>
> <li>ahmedabad</li>   
> <li>allahabad</li>   
> <li>amritsar</li>    
> <li>aurangabad</li>  
> <li>bangalore</li>   
> <li>bhopal</li>      
> <li>bhubaneshwar</li>
> <li>chandigarh</li>  
> <li>chennai</li>     
> <li>delhi</li>       
> <li>ghaziabad</li>   
> <li>goa</li>
> <li>gurgaon</li>
> <li>guwahati</li>
> <li>hyderabad</li>
> <li>jaipur</li>
> <li>jammu</li>
> <li>kanpur</li>
> <li>kolkata</li>
> <li>lucknow</li>
> <li>ludhiana</li>
> <li>meerut</li>
> <li>mumbai</li>
> <li>muzaffarnagar</li>
> <li>muzaffarpur</li>
> <li>nagpur</li>
> <li>noida</li>
> <li>others  //will contain the news for other cities which are not mentioned here</li> 
> <li>patna</li>
> <li>pune</li>
> <li>srinagar</li>
> <li>surat</li>
> <li>thiruvananthapuram</li>
> </ol>
> </p>

<br>
<p>This endpoint has the below two keys which you can use to get the more specific News with the content you wish to get.</p>

Key | Name |Example
---------|----------|---------
 city | name of the city you wish to get the news | https://ndtvnews-api.herokuapp.com/cities?city=values(chennai,mumbai,delhi)
 field | field content | https://ndtvnews-api.herokuapp.com/cities?field=values(headline,image_url,posted_date)
<br>

<h4>GET REQUEST :-</h4>
<br>

```
https://ndtvnews-api.herokuapp.com/cities?city=values(chennai,mumbai,delhi)&field=values(headline,image_url,posted_date)
```

<h4>OUTPUT :-</h4>
<br>

```JSON
{
    "news": [
        {
            "category": "chennai",
            "total_results": 200,
            "articles": [
                {
                    "headline": "Lioness Died Of Suspected SARS-CoV2, 8 Lions Infected At Chennai Zoo",
                    "image_url": "https://c.ndtvimg.com/2018-10/rmmns24g_lioness_120x90_21_October_18.jpg",
                    "posted_date": "2021-06-04"
                }
            ]
        },
        {
            "category": "mumbai",
            "total_results": 200,
            "articles": [
                {
                    "headline": "Air Force Bus Meets With Accident In Mumbai, 5 Injured",
                    "image_url": "https://i.ndtvimg.com/i/2017-08/hospital-generic-file_240x180_51502360464.jpg",
                    "posted_date": "2021-03-16"
                },
                {
                    "headline": " Actor Pearl Puri Arrested For Allegedly Raping Minor: Report",
                    "image_url": "https://c.ndtvimg.com/2021-06/igfmjj2s_pearl-puri-instagram_120x90_05_June_21.jpg",
                    "posted_date": "2021-06-05"
                }
            ]
        },
        {
            "category": "delhi",
            "total_results": 200,
            "articles": [
                {
                    "headline": "Delhi Reports 414 Covid Cases, Lowest In Over 2 Months, 60 Deaths",
                    "image_url": "https://c.ndtvimg.com/2020-11/jj4ilhc_coronavirus-delhi-november-2020-pti-240_240x180_23_November_20.jpg",
                    "posted_date": "2021-06-05"
                },
                {
                    "headline": "2nd Covid Wave Peaked At 28,000 Cases A Day, 3rd Wave May Reach 37,000: Arvind Kejriwal",
                    "image_url": "https://c.ndtvimg.com/2021-05/plmda16_coronavirus-india-generic-pti_120x90_07_May_21.jpg",
                    "posted_date": "2021-06-05"
                }
            ]
        }
    ]
}
```
<br>
<p>
Hence, it will give you a dictionary with a key called news and the value containing a list of dictionaries (this dictionary will hold the requested city, total_results and the news data list) for the requested cities.
</p>
<p>
If you are not specifying any keys and just simply hit the endpoint, it will give you the top news from all the cities across India with all the available fields (category, headline, description, url, image_url,  posted_date).
</p>
<hr>
<h3>For https://ndtvnews-api.herokuapp.com/sports :-</h3>

<p>This will give you the news related to the below mentioned sports.</p>

> <p>
> <ol>
> <li>cricket</li>
> <li>football</li>
> <li>tennis</li>
> <li>formula-1</li>
> <li>hockey</li>
> <li>golf</li>
> <li>badminton</li>
> <li>chess</li>
> <li>kabaddi</li>
> <li>wrestling</li>
> <li>nba</li>
> <li>boxing</li>
> </ol>
> </p>
> 
<br>
<p>This endpoint has the below two keys which you can use to get the more specific News with the content you wish to get.</p>

Key | Name |Example
---------|----------|---------
 sport | name of the sport you wish to get the news| https://ndtvnews-api.herokuapp.com/sports?sport=values(cricket,football)
 field | field content | https://ndtvnews-api.herokuapp.com/sports?field=values(headline,description,url)
<br>

<h4>GET REQUEST :-</h4>
<br>

```
https://ndtvnews-api.herokuapp.com/sports?sport=values(cricket,football)&field=values(headline,description,url)
```

<h4>OUTPUT :-</h4>
<br>

```JSON
{
    "news": [
        {
            "category": "cricket",
            "total_results": 18,
            "articles": [
                {
                    "headline": "Ankeet Chavan Requests BCCI Through MCA To Issue Ban Revocation Letter",
                    "description": "Left-arm spinner Ankeet Chavan has requested the BCCI to issue his ban revocation letter which would allow him to return to competitive cricket.",
                    "url": "https://sports.ndtv.com//cricket/ankeet-chavan-requests-bcci-through-mca-to-issue-ban-revocation-letter-2457241"
                },
                {
                    "headline": "Rashid Khan Sums Up Virat Kohli In \"One Word\", Hails MS Dhoni In Special Tribute",
                    "description": "Entertaining fans via a Q&A session on Instagram, Rashid Khan glorified Virat Kohli, and had special praise for former India captain MS Dhoni.",
                    "url": "https://sports.ndtv.com//cricket/rashid-khan-sums-up-virat-kohli-in-one-word-hails-ms-dhoni-in-special-tribute-2456442"
                }
            ]
        },
        {
            "category": "football",
            "total_results": 18,
            "articles": [
                {
                    "headline": "FIFA World Cup Qualifiers: India Gears Up For Bangladesh Game After Qatar Loss",
                    "description": "After losing 1-0 to Qatar, the Indian football team will take on Bangladesh in the FIFA WC Qualifiers match on June 7.",
                    "url": "https://sports.ndtv.com//football/fifa-world-cup-qualifiers-india-gears-up-for-bangladesh-game-after-qatar-loss-2457028"
                },
                {
                    "headline": "Spain And Portugal In Lukewarm Stalemate Ahead Of European Championships",
                    "description": "Spain and Portugal both lacked firepower as they drew 0-0 in a friendly warm up for the European Championships at the Metropolitano in Madrid.",
                    "url": "https://sports.ndtv.com//football/spain-and-portugal-in-lukewarm-stalemate-ahead-of-euros-2020-2456805"
                },
                {
                    "headline": "World Cup Qualifiers: Retaken Neymar Penalty Helps Brazil Maintain Perfect Start",
                    "description": "Richarlison had given Brazil the lead on 64 minutes and Neymar sealed the win deep into injury time, but only after another VAR farce.",
                    "url": "https://sports.ndtv.com//football/world-cup-qualifiers-retaken-neymar-penalty-helps-brazil-maintain-perfect-start-2456792"
                }
            ]
        }
    ]
}
```
<br>
<p>
Hence, it will give you a dictionary with a key called news and the value containing a list of dictionaries (this dictionary will hold the requested sport, total_results and the news data list) for the requested sports.
</p>
<p>
If you are not specifying any keys and just simply hit the endpoint, it will give you the top cricket news with all the available fields (category, headline, description, url, image_url,  posted_date).
</p>
<hr>

<h2>Installation and Setup</h2>

All dependencies are listed in _requirements.txt_ file.

1. To install dependencies, run -

    ```bash
    $ pip install -r requirements.txt
    ```

2. Database - 

        It will take considerable amount of time to scrap all the data present in NDTV website in live time for each request. So, HEROKU POSTGRES DB (flask sqlite can also be used) has been used to store the scrapped data. The database will be feed with latest news present in the NDTV website for every 10 minutes which inturn will feed a pandas dataframe. 

        Once a request is received, it will query the dataframe for the requested data and will provide the JSON response.

3. Start the api server - 
    ```bash
    $ python app.py
    ```
<hr>

<h2>Contributing</h2>
<p>I am a newbie and this is my First Project in Flask API and also in Github. So, advices, corrections, suggestions and pull requests are happily welcome and let us engage in <a href = "https://github.com/NishanthMuruganantham/ndtv-api/discussions">discussions</a></p>
<p>For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.</P>

©<a href="https://github.com/NishanthMuruganantham">Nishanth</a>
