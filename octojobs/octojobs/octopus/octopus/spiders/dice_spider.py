"""Module for our initial spider."""
import scrapy
import re
from octopus.items import OctopusItem


class DiceSpider(scrapy.Spider):
    """Crawl each url in start_urls.

    parse(self, response) is the default callback method for the Spider class
    for parsing the response object using CSS/x-path and yield an object of type
    OctopusItem to the pipeline.
    """

    name = "dice"

    start_urls = [
    'https://www.dice.com/jobs/q-Go-jtype-Contract+Independent-limit-30-l-Seattle-radius-30-jobs.html?searchid=2018379535598'
    ]

    def parse(self, response):
        """Default callback used by Scrapy to process downloaded responses."""
        dice_company_dict = {}

        for element in response.css('div.serp-result-content'):
            """Grab items using css selectors and x-paths."""
            anchor = element.css('a.dice-btn-link').extract_first()
            title = element.css(
                'a.dice-btn-link.loggedInVisited::text').extract_first()
            url = re.search(
                r'href="([^"]*)"', anchor).group(1)
            company = element.css(
                'ul.list-inline li.employer a.dice-btn-link::text').extract_first()
            description = ' '.join(element.css(
                'div.shortdesc::text').extract_first().split())
            city = element.css(
                'ul.list-inline li.location::text').extract_first()

            """Set up dictionary for Dice job info"""

            dice_company_dict[url] = {
                'url': url,
                'title': title,
                'company': company,
                'description': description,
                'city': city
            }


        #commented out below functionalty to try to parse the description
        #because it's broken
        # """Follow each link, and build items to pass to pipeline."""
        #
        # for key in dice_company_dict:
        #     import pdb; pdb.set_trace()
        #     yield scrapy.Request(key)
        #
        #     dice_company_dict[key]['description'] = response.css(
        #             'div.highlight-black::text').extract_first()
        #     continue

        items = {key : OctopusItem(dice_company_dict[key]) for key in dice_company_dict.keys()}
        # import pdb; pdb.set_trace()
        yield items
