import os

from twisted.python.failure import Failure
from scrapy.exceptions import NotConfigured
from scrapy.dupefilters import RFPDupeFilter


_middleware = None


class Dupefiltered(RuntimeError):
    def __init__(self, request):
        self.request = request


class ErrbackDupefilter(RFPDupeFilter):
    def request_seen(self, request):
        fp = self.request_fingerprint(request)
        if fp in self.fingerprints:
            if _middleware and request.errback:
                _middleware.queues.append(
                    request.errback(Failure(Dupefiltered(request)))
                )
            return True
        self.fingerprints.add(fp)
        if self.file:
            self.file.write(fp + os.linesep)


class ErrbackDupefilterMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('ERRBACK_DUPEFILTER_ENABLED'):
            raise NotConfigured
        return cls(crawler)

    def __init__(self, crawler):
        global _middleware
        _middleware = self
        self.queues = []

    def process_spider_output(self, response, result, spider):
        for x in result:
            yield x
        queues, self.queues = self.queues, []
        for queue in queues:
            for x in queue:
                yield x
