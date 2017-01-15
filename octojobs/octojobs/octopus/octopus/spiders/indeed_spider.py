"""Module for our initial spider."""
import scrapy
import re
from octopus.items import OctopusItem


class IndeedSpider(scrapy.Spider):
    """Crawl each url in start_urls.

    parse(self, response) is the default callback method for the Spider class
    for parsing the response object using CSS/x-path and yield an object of type
    OctopusItem to the pipeline.
    """

    name = "indeed"

    start_urls = [
    #just one url with only a few jobs to demonstrate proof of concept.
    #add more urls but you will be given fake data pretty quickly if you
    #crawl too much. Better do one url with a few jobs at a time rather threadName
    #casting a wide net if that net doesn't catch anything meaningful.
    'https://www.indeed.com/jobs?q=secdb&l=New+York%2C+NY', #7 jobs
    'https://www.indeed.com/jobs?q=golang&l=Seattle%2C+WA', #~50 jobs
    'https://www.indeed.com/jobs?q=python+finance&l=Seattle%2C+WA' #~140 jobs
    ]

    def parse(self, response):
        """Default callback used by Scrapy to process downloaded responses."""
        items = {}
        company_dict = {}

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
                company_dict[url] = {
                    'url': url,
                    'title': title,
                    'company': company,
                    'description': description,
                    'city': city
                }

            #commented out below functionalty to try to parse the description
            #because it's broken
            """Follow each link, and build items to pass to pipeline."""
            # for key in company_dict:
            #     yield scrapy.Request(key)
            #
            #     company_dict[key]['description'] = response.css(
            #         'span.summary::text').extract_first()
            #     self.build_items(items, company_dict, key)
            #     continue

            """Find the next page of job postings. Go there and call parse."""
            next_page = response.css(
                'div.pagination a::attr(href)').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)


            """put OctopusItems in items for the pipeline to pick up."""
            items = {key : OctopusItem(company_dict[key]) for key in company_dict.keys()}
            yield items
