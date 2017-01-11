"""Module for our initial spider."""
import scrapy
import re
from octopus.items import OctopusItem


class JobSpider(scrapy.Spider):
    """Crawl each url in start_urls and extract data.
    Data will be ported into pipelines as OctopusItem instances.
    Pipelines will find each item instance and pass it to the database.

    create_dict(self, iter, url, title, company, city, description) creates and
    returns a new empty dictionary for each job site and populates with data
    pulled by using css selectors and x-paths.

    build_items(self, items, iter, key) takes the dictionaries created, and
    creates and returns OctopusItem instances from them.

    parse(self, response) is the default callback method for the Spider class.
    It takes in the HTTP response, pulls data from html tags using CSS/ x-path
    selectors, and uses that data to create item instances. The pipelines.py
    file takes in those item instances and ports them to the database.

    And run the parse method on each of them.
    """

    name = "jobs"

    start_urls = [
        # 'file:///Users/rachaelwisecarver/codefellows/401/octojobs/Octojobs/octojobs/octojobs/octopus/indeed_list_view.html'
        # 'file:///Users/rachaelwisecarver/codefellows/401/octojobs/Octojobs/octojobs/octojobs/octopus/dice_list_view.html',
        'https://www.indeed.com/jobs?q=python&l=seattle%2C+wa',
        'https://www.indeed.com/jobs?q=javascript&l=seattle%2C+wa',
        'https://www.indeed.com/jobs?q=ios&l=seattle%2C+wa',
        'https://www.indeed.com/jobs?q=back+end&l=seattle%2C+wa',
        'https://www.indeed.com/jobs?q=front+end&l=seattle%2C+wa',
        'https://www.indeed.com/jobs?q=full+stack&l=seattle%2C+wa',
        'https://www.indeed.com/jobs?q=data+scientist&l=seattle%2C+wa',
        'https://www.indeed.com/jobs?q=python&l=San+Francisco+Bay+Area%2C+CA',
        'https://www.indeed.com/jobs?q=javascript&l=San+Francisco+Bay+Area%2C+CA',
        'https://www.indeed.com/jobs?q=ios&l=San+Francisco+Bay+Area%2C+CA',
        'https://www.indeed.com/jobs?q=back+end&l=San+Francisco+Bay+Area%2C+CA',
        'https://www.indeed.com/jobs?q=front+end&l=San+Francisco+Bay+Area%2C+CA',
        'https://www.indeed.com/jobs?q=full+stack&l=San+Francisco+Bay+Area%2C+CA',
        'https://www.indeed.com/jobs?q=data+scientist&l=San+Francisco+Bay+Area%2C+CA',
        'https://www.indeed.com/jobs?q=python&l=New+York%2C+NY',
        'https://www.indeed.com/jobs?q=javascript&l=New+York%2C+NY',
        'https://www.indeed.com/jobs?q=ios&l=New+York%2C+NY',
        'https://www.indeed.com/jobs?q=back+end&l=New+York%2C+NY',
        'https://www.indeed.com/jobs?q=front+end&l=New+York%2C+NY',
        'https://www.indeed.com/jobs?q=full+stack&l=New+York%2C+NY',
        'https://www.indeed.com/jobs?q=data+scientist&l=New+York%2C+NY',
        'https://www.dice.com/jobs?q=&l=seattle%2C+WA',
        'https://www.dice.com/jobs?q=&l=San+Francisco+Bay+Area%2C+CA',
        'https://www.dice.com/jobs?q=&l=New+York%2C+NY',
    ]

    def create_dict(self, iter, url, title, company, city, description):
        """Takes in an empty dictionary, and the items pulled from html.
        Creates a new dictionary within that dictionary holding these items."""
        iter[url] = {}
        iter[url]['url'] = url
        iter[url]['title'] = title
        iter[url]['company'] = company
        iter[url]['city'] = city
        iter[url]['description'] = description
        return iter

    def build_items(self, items, iter, key):
        """Takes in a dictionary and a dict key.
        Returns an instance of the item class, to be passed to pipelines."""

        items[key] = OctopusItem(
                        title=iter[key]['title'],
                        url=iter[key]['url'],
                        company=iter[key]['company'],
                        city=iter[key]['city'],
                        description=iter[key]['description'],
                    )
        return items

    def parse(self, response):
        """Default callback used by Scrapy to process downloaded responses."""
        items = {}
        company_dict = {}
        dice_company_dict = {}

        if response.xpath('//*[@id="resultsCol"]'):
            """Search through Indeed list view for links to jobs."""

            for element in response.css('div.result h2.jobtitle'):
                """Grab items using css selectors and x-paths."""

                anchor = element.css('a.turnstileLink').extract_first()
                title = re.search(r'title="([^"]*)"', anchor).group(1)
                base_url = 'https://www.indeed.com'
                url = base_url + re.search(
                    r'href="([^"]*)"', anchor).group(1)
                data = response.css('div.result span.company')
                if data.css('span a'):
                    company = data.css('span a::text').extract_first()
                else:
                    company = data.css('span::text').extract_first()
                company = ' '.join(company.split())
                city = response.css(
                    'div.result span.location::text').extract_first()
                description = response.css(
                    'div.result span.summary::text').extract_first()

                """Set up dictionary for Indeed job info"""
                self.create_dict(
                    company_dict,
                    url,
                    title,
                    company,
                    city,
                    description)

            """Follow each link, and build items to pass to pipeline."""
            for key in company_dict:
                yield scrapy.Request(key)

                if not response.xpath('//*[@id="job-content"]'):
                    self.build_items(items, company_dict, key)
                    continue

                else:
                    company_dict[key]['description'] = response.css(
                        'span.summary::text').extract_first()
                    self.build_items(items, company_dict, key)
                    continue

            """Find the next page of job postings. Go there and call parse."""
            next_page = response.css(
                'div.pagination a::attr(href)').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)

        elif response.xpath('//*[@id="resultSec"]'):
            """If the site is dice.com - do the same thing as above."""

            for element in response.css('div.serp-result-content'):
                """Grab items using css selectors and x-paths."""
                # import pdb;pdb.set_trace()
                anchor = element.css('a.dice-btn-link').extract_first()
                # title = re.search(r'title="([^"]*)"', anchor).group(1)
                title = element.css(
                    'a.dice-btn-link.loggedInVisited::text').extract_first()
                url = re.search(
                    r'href="([^"]*)"', anchor).group(1)
                company = element.css(
                    'ul.list-inline a.dice-btn-link::text').extract_first()
                description = ' '.join(element.css(
                    'div.shortdesc::text').extract_first().split())
                city = element.css(
                    'ul.list-inline li.location::text').extract_first()

                """Set up dictionary for Dice job info"""
                self.create_dict(
                    dice_company_dict,
                    url,
                    title,
                    company,
                    city,
                    description)

            """Follow each link, and build items to pass to pipeline."""
            for key in dice_company_dict:
                yield scrapy.Request(key)

                if not response.xpath('//*[@id="bd"]'):
                    self.build_items(items, dice_company_dict, key)
                    continue

                else:
                    dice_company_dict[key]['description'] = response.css(
                        'div.highlight-black::text').extract_first()
                    self.build_items(items, dice_company_dict, key)
                    continue

        yield items
