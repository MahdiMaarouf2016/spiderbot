import tldextract
from urllib.parse import urlparse


def getDomaineName(url):
    return tldextract.extract(url).domain


def getDomaine(url):
    extracted_domain = tldextract.extract(url)
    return "{}.{}".format(extracted_domain.domain, extracted_domain.suffix)


def getScheme(url):
    return urlparse(url).scheme


def getSuffix(url):
    return tldextract.extract(url).suffix


def getPath(url):
    return urlparse(url).path


def getNetWorkLocation(url):
    return urlparse(url).netloc
def getBaseUrl(url):
    return getScheme(url) + "://" + getDomaine(url)