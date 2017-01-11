# -*- coding: utf-8 -*-
"""Define here the models for your scraped items.

See documentation in:
http://doc.scrapy.org/en/latest/topics/items.html
"""

import scrapy


class OctopusItem(scrapy.Item):
    """Make model for job information."""

    title = scrapy.Field()
    url = scrapy.Field()
    company = scrapy.Field()
    city = scrapy.Field()
    description = scrapy.Field()
