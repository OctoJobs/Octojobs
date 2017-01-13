#OCTOJOBS#

![logo](octojobs/static/images/logo.png) 

Deployed on Heroku as [octojobs-cf](octojobs-cf.herokuapp.com)


Octojobs is an open source webscraper and job opportunity aggregator. It scrapes a jobboard website, such as Indeed or Dice.com, and returns a query of jobs based on user-provided keywords and locations.

Our scraper stores the results of a scrape in a postgreSQL database. The results are then loaded into the views, so that users can see job titles with live links to their original postings, the employer name, the location, and a brief description of the opportunity.

##Mission Statement
Get more reach for your job search.

Our goal was to build a scraper that would target multiple sites and aggregate their data in one location that would be easy for a user to query.

## User Stories
###User
As a user, we want an easy, one stop shop for our job search to find a job. 

As a user, we want a clear way to sort through the data for the exact information we want.

As a user, we want a straightforward, beautiful user experience to make the retieval of information easy.

As a user, we want to search for specific skills and job titles. 

###Developer
As a developer, we want to build elegant, readable code with optimal time complexity.

As a developer, we want to gain experience managing large data sets and queries.

As a developer, we want to gather data on what jobs and skills are in the highest demand.

As a developer, we want to learn webscraping and data cleaning techniques.


## About the Hackers

This app was created in 4 days by the lovely and talented:

[Claire Gatenby](https://github.com/clair3st)
[Colin Lamont](https://github.com/chamberi)
[Marc Kessler-Wenicker](https://github.com/wenima)
[Rachael Wisecarver](https://github.com/rwisecar)


## Development Environment
The development environment will include:
1. Testing packages, including pytest, pytest-cov, Tox, and webtest to aid in test driven development.
2. Scrapy
3. The Python Requests library.
4. Lots and lots of coffee.

If you would like to clone or contribute to, this repo, please follow these steps:
1. Clone the repo into a directory on your terminal.
2. Create a virtual environment
3. Install the required packages:
```
pip install -e .
```
or
```
pip install -e .[testing]
```

## Third Party Resources
We would like to thank the following libraries, frameworks, packages, resources, and people.
1. [Scrapy](https://doc.scrapy.org/en/latest/)
2. Pyramid
3. postgreSQL
4. Heroku
5. Waffle
6. Bootstrap
7. [Github user econchick and her NewCoder Blog](http://newcoder.io/scrape/)
8. [Stack Overflow](http://stackoverflow.com/questions/6456304/scrapy-unit-testing/12751649)
9. fake_Useragent
10. [Scrapehero.com](https://www.scrapehero.com/how-to-prevent-getting-blacklisted-while-scraping/)

## Tox Coverage Reports
```
---------- coverage: platform darwin, python 2.7.11-final-0 ----------
Name                                                           Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------
octojobs/__init__.py                                              11      8    27%   8-15
octojobs/models/__init__.py                                       22      0   100%
octojobs/models/meta.py                                            5      0   100%
octojobs/models/mymodel.py                                        11      0   100%
octojobs/octojobs/octopus/octopus/__init__.py                      0      0   100%
octojobs/octojobs/octopus/octopus/items.py                         8      0   100%
octojobs/octojobs/octopus/octopus/middlewares.py                  18     10    44%   19-21, 28, 35-36, 44, 52-53, 56
octojobs/octojobs/octopus/octopus/pipelines.py                    27     16    41%   17, 23, 38-40, 44-57
octojobs/octojobs/octopus/octopus/settings.py                     18      0   100%
octojobs/octojobs/octopus/octopus/spiders/__init__.py              0      0   100%
octojobs/octojobs/octopus/octopus/spiders/practise_spider.py      12      6    50%   15-22, 28-30
octojobs/octojobs/octopus/octopus/spiders/spider.py               65     47    28%   82-178
octojobs/routes.py                                                 5      0   100%
octojobs/scripts/__init__.py                                       0      0   100%
octojobs/scripts/initializedb.py                                  28     18    36%   22-25, 29-55
octojobs/views/__init__.py                                         0      0   100%
octojobs/views/default.py                                         61      0   100%
--------------------------------------------------------------------------------------------
TOTAL                                                            291    105    64%


=================================================================================== 32 passed in 2.81 seconds ===================================================================================


---------- coverage: platform darwin, python 3.5.2-final-0 -----------
Name                                                           Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------
octojobs/__init__.py                                              11      8    27%   8-15
octojobs/models/__init__.py                                       22      0   100%
octojobs/models/meta.py                                            5      0   100%
octojobs/models/mymodel.py                                        11      0   100%
octojobs/octojobs/octopus/octopus/__init__.py                      0      0   100%
octojobs/octojobs/octopus/octopus/items.py                         8      0   100%
octojobs/octojobs/octopus/octopus/middlewares.py                  18     10    44%   19-21, 28, 35-36, 44, 52-53, 56
octojobs/octojobs/octopus/octopus/pipelines.py                    27     16    41%   17, 23, 38-40, 44-57
octojobs/octojobs/octopus/octopus/settings.py                     18      0   100%
octojobs/octojobs/octopus/octopus/spiders/__init__.py              0      0   100%
octojobs/octojobs/octopus/octopus/spiders/practise_spider.py      12      6    50%   15-22, 28-30
octojobs/octojobs/octopus/octopus/spiders/spider.py               65     47    28%   82-178
octojobs/routes.py                                                 5      0   100%
octojobs/scripts/__init__.py                                       0      0   100%
octojobs/scripts/initializedb.py                                  28     18    36%   22-25, 29-55
octojobs/views/__init__.py                                         0      0   100%
octojobs/views/default.py                                         61      0   100%
--------------------------------------------------------------------------------------------
TOTAL                                                            291    105    64%

=================================================================================== 32 passed in 4.00 seconds ===================================================================================
```
