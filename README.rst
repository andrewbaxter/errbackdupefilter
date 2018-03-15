By default duplicate requests in Scrapy will be silently dropped.  This extension causes dropping requests to trigger the errback.

Installation
############

Run::

   pip install git+https://github.com/andrewbaxter/scrapy-errbackdupefilter

Add this to ``SPIDER_MIDDLEWARES``::

   SPIDER_MIDDLEWARES = {
       'errbackdupefilter.ErrbackDupefilterMiddleware': 2000,
   }

Add these lines to ``settings.py``::

   DUPEFILTER_CLASS = 'errbackdupefilter.ErrbackDupefilter'
   ERRBACK_DUPEFILTER_ENABLED = True

Example usage
#############

The spider::

   import scrapy
   from scrapy.http import Request
   from errbackdupefilter import Dupefiltered

   class ScrapinghubSpider(scrapy.Spider):
       name = "scrapinghub"
       allowed_domains = ["scrapinghub.com"]
       start_urls = (
           'http://www.scrapinghub.com/',
       )

       def parse(self, response):
           return Request(
               self.start_urls[0],
               callback=self.parse2)

       def parse2(self, response):
           return Request(
               self.start_urls[0],
               callback=self.parse3,
               errback=self.errback)

       def parse3(self, response):
           pass

       def errback(self, failure):
           failure.trap(Dupefiltered)
           print('filtered {}'.format(failure.value.request))

when run with::

   scrapy crawl scrapinghub

will output::

   filtered <GET http://www.scrapinghub.com/>
