from twisted.python.failure import Failure
from scrapy.dupefilters import RFPDupeFilter

class Dupefiltered(RuntimeError):
    def __init__(self, request):
        self.request = request

class ErrbackDupefilter(RFPDupeFilter):
    def request_seen(self, request):
        fp = self.request_fingerprint(request)
        if fp in self.fingerprints:
            if request.errback:
                request.errback(Failure(Dupefiltered(request)))
            return True
        self.fingerprints.add(fp)
        if self.file:
            self.file.write(fp + os.linesep)
