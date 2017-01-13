![OctoJobs](octojobs/static/images/logo.png) #OCTOJOBS#
## Deployed at: octojobs-cf.herokuapp.com

Octojobs is an open source webscraper and job opportunity aggregator. It scrapes a jobboard website, such as Indeed or Dice.com, and returns a query of jobs based on user-provided keywords and locations.

Our scraper stores the results of a scrape in a postgreSQL database. The results are then loaded into the views, so that users can see job titles with live links to their original postings, the employer name, the location, and a brief description of the opportunity.

##Mission Statement
Get more reach for your job search.

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
