import trafilatura as tr

def get_content(url):
    raw_html = tr.fetch_url(url)
    extracted_text = tr.extract(raw_html)
    # create a dictionary of the url, raw_html, and extracted_text
    response_dict = {'url': url, 'raw_html': raw_html, 'extracted_text': extracted_text}
    return response_dict

def get_content_from_raw(raw_html):
    extracted_text = tr.extract(raw_html)
    return extracted_text

def get_content_from_url(url):
    # get raw html
    raw_html = tr.fetch_url(url)
    # return raw html
    return raw_html