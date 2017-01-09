"""Module for our initial spider."""
import scrapy
import json


class JobSpider(scrapy.Spider):
    """Job Spider with website URL."""

    name = "jobs"

    # def start_requests(self):
    """Foo."""
    start_urls = [
        'file:///Users/colinlamont/codefellows/python/lab-work/Octojobs/octojobs/octojobs/octopus/test.html',
    ]

        # for url in start_urls:
        #     yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """It parses the response and grabs the title, url, company, location, and summary."""

        for job in response.xpath('//*[@id="job-content"]'):
            yield {
                'title': job.css('b.jobtitle::text').extract_first(),
                'url': job.css('div.result-link-bar a.ws_label a::attr(href)').extract_first(),
                'company': job.css('span.company::text').extract_first(),
                'location': job.css('span.location::text').extract_first(),
                'summary': job.css('span.summary::text').extract_first(),
            }

        # test_file = 'output.json'
        # with open(test_file, "w") as f:
        #     f.write(json.dumps(new_dict))

    # for data in parse(response):
    #     {}
