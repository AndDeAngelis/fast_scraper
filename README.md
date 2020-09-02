# Fast Scraper

Fast Scraper is a didactic project to scrape soccer odds from betexplorer (www.betexplorer.com). Just create one or more txt file containing urls to scrape (you can see an example inside the 'input-files' folder) and run! It will generate as output a pickle for each url; each pickle is the binarized version of a list of JSONs, where each JSON represents a soccer match.

Example of information scraped from a single match:
```
{
    "basic_info":{
        "match_date":"21.05.2017",
        "nation":"England",
        "league":"Premier League 2016/2017",
        "match_name":"Arsenal - Everton",
        "result":"3:1",
        "odds_url":"https://www.betexplorer.com/soccer/england/premier-league-2016-2017/arsenal-everton/SGPa5fvr/"
    },
    "odds":{
        "home_win":{
            "10Bet":{
                "14,05,2017,09,55":"1.54",
                "21,05,2017,15,52":"1.35"
            },
            ...
        },
        "draw":{
            "10Bet":{
                "14,05,2017,09,55":"4.15",
                "21,05,2017,15,52":"5.80"
            },
            ...
        },
        "away_win":{
            "10Bet":{
                "14,05,2017,09,55":"5.80",
                "21,05,2017,15,52":"7.75"
            },
            ...
        },
        "over_25":{
            "10Bet":{
                "14,05,2017,18,29":"1.61",
                "21,05,2017,15,29":"1.35"
            ...
        },
        "under_25":{
            "10Bet":{
                "14,05,2017,18,29":"2.15",
                "21,05,2017,15,29":"3.10"
            },
            ...
        },
        "goal":{
            "10Bet":{
                "14,05,2017,18,11":"1.80",
                "21,05,2017,15,18":"1.61"
            },
            ...
        },
        "no_goal":{
            "10Bet":{
                "14,05,2017,18,11":"2.00",
                "21,05,2017,15,29":"2.30"
            },
            ...
        }
    }
}
```

## Prerequisites

* Python 3 and pip installed
* Files containing urls to scrape placed inside 'input-files' directory
* Chromedriver for your OS - browser verion placed inside 'chromedriver' directory

## Getting started

* Clone the project

`git clone https://github.com/AndDeAngelis/fast_scraper.git`

* Create a virtual environment with Python 3.* and activate it

```
python3 -m venv ./venv
source venv/bin/activate
```

* Install dependencies

`pip install -r requirements.txt`

* Run

`python main.py`

At the end of the execution will be created one pickle for each scraped url. The pickles will be saved inside the 'output-pickles' directory.

## Check pickles

After the scraping you can check the pickles and generate a report in which you can see how many odds are missing, e.g.:

> england_premier-league-2016-2017.pkl  
Matches: 380  
Home: 15  
Draw: 15  
Away: 15  
Over: 375  
Under: 375  
Goal: 375  
No Goal: 375  

Scraping the england premier league, season 2016-2017, ends up in scraping 380 matches. Only 15 out of 380 have home win, draw and away win odds. Instead, 375 out of 380 have under/over and goal/no goal odds.

## To-do list

- [ ] Solve the extraction problem for home win, draw and away win markets.
