# %%

from urllib.parse import urlparse


def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        return results[-2] + '.' + results[-1]
    except:
        return ''


# Get sub domain name (name.example.com)
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc.replace("www.", "")
    except:
        return ''


def edit_url(link, parent_link):
    link_parsed = urlparse(link)
    parent_parsed = urlparse(parent_link)

    if link_parsed.netloc == '':
        parent_loc = parent_parsed.netloc.replace("www.", '') if parent_parsed.netloc.startswith(
            "www.") else parent_parsed.netloc
        new_link = link_parsed._replace(scheme='https', netloc=parent_loc)
    else:
        new_link = link_parsed._replace(
            scheme='https', netloc=link_parsed.netloc.replace("www.", ''))
    return new_link.geturl().rstrip('/')
