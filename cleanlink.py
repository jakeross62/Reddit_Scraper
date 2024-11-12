from url_cleaner import UrlCleaner
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode, quote


#link cleaner, just parse uncleaned link through clean_link 
def clean_link(link):
    parts = urlparse(link)
    link2 =urlunparse(parts._replace(path=quote(parts.path)))
    parsed = urlparse(link2)
    qd = parse_qs(parsed.query, keep_blank_values=True)
    filtered = dict( (k, v) for k, v in qd.items() if not k.startswith('utm_'))
    newurl = urlunparse([
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        urlencode(filtered, doseq=True), 
        parsed.fragment
    ])
    c = UrlCleaner() 
    cleaned = c.clean(newurl) 

    return cleaned