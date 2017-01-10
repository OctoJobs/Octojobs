"""Module for our initial spider."""
import scrapy
import json
import re


class JobSpider(scrapy.Spider):
    """Job Spider with website URL."""

    name = "jobs"
    allowed_domains = ["indeed.com"]

    start_urls = [
        # 'file:///Users/colinlamont/codefellows/python/lab-work/Octojobs/octojobs/octojobs/octopus/test.html',
        # 'file:///Users/rachaelwisecarver/codefellows/401/octojobs/Octojobs/octojobs/octojobs/octopus/test.html',
        # 'file:///Users/rachaelwisecarver/codefellows/401/octojobs/Octojobs/octojobs/octojobs/octopus/indeed_list_view.html',
        'https://www.indeed.com/jobs?q=developer&l=seattle%2C+wa',
    ]

    def parse(self, response):
        """Check the response to see if there is the information we need.
        If not, grab the link and go to that page and run again.
        Otherwise, yield the data we want as JSON."""

        if not response.xpath('//*[@id="job-content"]'):
            if response.xpath('//*[@id="resultsCol"]'):
                url_list = []
                for item in response.xpath('//*[@id="resultsCol"]'):
                    anchor = item.css('div.result h2.jobtitle a.turnstileLink').extract_first()
                    url = re.search(r'href="([^"]*)"', anchor).group(1)
                    base_url = 'https://www.indeed.com'
                    base_url += url
                    url_list.append(base_url)
                for url in url_list:
                    yield scrapy.Request(url)
            else:
                print("Sorry, file not found.")
        elif response.xpath('//*[@id="job-content"]'):
            for job in response.xpath('//*[@id="job-content"]'):
                yield {
                    'title': job.css('font::text').extract_first(),
                    'url': job.xpath('//*[@id="p_c7e367148ce1fe2b"]/span/a/@href').extract_first(),
                    'company': job.css('span.company::text').extract_first(),
                    'location': job.css('span.location::text').extract_first(),
                    'summary': job.css('span.summary::text').extract_first(),
                }
        # else:
        #     yield scrapy.Request(start_urls)
