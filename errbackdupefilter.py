import os

from twisted.python.failure import Failure
from scrapy.dupefilters import RFPDupeFilter


class Dupefiltered(RuntimeError):
    def __init__(self, request):
        self.request = request


class ErrbackDupefilter(RFPDupeFilter):
    def request_seen(self, request):
        global _middleware
        if not _middleware:
            raise AssertionError(
                'You must configure ErrbackDupefilterMiddleware')
        fp = self.request_fingerprint(request)
        if fp in self.fingerprints:
            if request.errback:
                _middleware.queues.append(
                    request.errback(Failure(Dupefiltered(request)))
                )
            return True
        self.fingerprints.add(fp)
        if self.file:
            self.file.write(fp + os.linesep)


class ErrbackDupefilterMiddleware(object):
    def __init__(self):
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
