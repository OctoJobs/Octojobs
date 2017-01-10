"""Module for our initial spider."""
import scrapy
import json
import re


class JobSpider(scrapy.Spider):
    """Job Spider with website URL."""

    name = "jobs"
    # allowed_domains = ["indeed.com"]

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

        company_dict = {}
        if not response.xpath('//*[@id="job-content"]'):
            if response.xpath('//*[@id="resultsCol"]'):
                # url_list = []
                # title_list = []
                # company_list = []

                for element in response.css('div.result h2.jobtitle'):
                    
                    anchor = element.css('a.turnstileLink').extract_first()
                    title = re.search(r'title="([^"]*)"', anchor).group(1)

                    base_url = 'https://www.indeed.com'
                    url = base_url + re.search(r'href="([^"]*)"', anchor).group(1)
                    company_dict[url] = {}
                    company_dict[url]['url'] = url
                    company_dict[url]['title'] = title

                    data = response.css('div.result span.company')
                    # import pdb;pdb.set_trace()
                    if data.css('span a'):
                        company = data.css('span a::text').extract_first()
                    else:
                        company = data.css('span::text').extract_first()
                    company = ' '.join(company.split())
                    company_dict[url]['company'] = company

                for key in company_dict:
                    yield scrapy.Request(key)

                    if not response.xpath('//*[@id="job-content"]'):
                        for key in company_dict:
                            yield {
                                'title': company_dict[key]['title'],
                                'url': company_dict[key]['url'],
                                'company': company_dict[key]['company'],
                                # location = element.css('span.location span::text').extract_first()
                                # summary = element.css('span.summary::text').extract_first()
                            }
                            continue
            elif response.xpath('//*[@id="job-content"]'):
                for job in response.xpath('//*[@id="job-content"]'):
                    # import pdb; pdb.set_trace()
                    yield {
                        'title': job.css('font::text').extract_first(),
                        'url': response.url,
                        'company': job.css('span.company::text').extract_first(),
                        'location': job.css('span.location::text').extract_first(),
                        'summary': job.css('span.summary::text').extract_first(),
                    }


        next_page = response.css('div.pagination a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
