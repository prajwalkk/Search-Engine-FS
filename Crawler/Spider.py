import requests
from bs4 import BeautifulSoup, Comment


def filter_tags(element):
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head',
        'input',
        'script',
        'style'
    ]
    if element.parent.name not in blacklist:
        return True
    return False


def connect_page(url):
    # Connect to a page. Try again after 2 seconds
    header = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0"}
    try:
        response = requests.get(url, timeout=(
            5, 30), allow_redirects=True, headers=header)
    except requests.RequestException:
        return None
    return response


def scrape_links(html):
    soup = BeautifulSoup(html, features='html.parser')
    links = soup.find_all('a', href=True)
    return links


def extract_data(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    comments = soup.findAll(text=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()
    for div in soup.find_all("div", {'class': 'browser-stripe'}):
        div.decompose()
    texts = soup.find_all(text=True)
    filtered_text = filter(filter_tags, texts)
    return " ".join([i.strip() for i in filtered_text]).encode('utf-8', errors='ignore').decode('utf-8')


def write_data_to_file(html, url, file_id):
    extracted_text = extract_data(html)
    if extracted_text == '':
        raise ValueError
    with open(file_id, 'w', errors='ignore', encoding='utf-8') as f:
        f.write(url.strip('/') + "\n")
        f.write(extracted_text)
