import logging
import time
from collections import deque
from datetime import datetime
from pathlib import Path
from pathlib import PosixPath

import networkx as nx

from Domain import get_domain_name, edit_url
from GenerateGraph import add_edges, save_graph
from Spider import *

MAX_COUNT = 7000
BASE_URL = "https://cs.uic.edu/"
DOMAIN = "uic.edu"
BLACK_LIST = ['.gif', '.jpeg', '.jpg', '.ps', '.ppt', '.mp4',
              '.mp3', '.svg', 'mailto:', 'favicon', '.ico',
              '.css', '.apk', '.js', '.png', '.gif', '.pdf',
              '.doc', '@', 'tel']

try:
    currpath = str(Path(__file__).parents[1])
    print(currpath)
except IndexError:
    print("Please execute this from the parent folder. Run 'python Crawler/main.py'")
    exit()

date_now = str(datetime.now().strftime('%Y%m%d'))
PROJECT_PATH = currpath + '/DataFiles/CrawledData/' + date_now + '/'
OUTLINK_PATH = currpath + '/DataFiles/Links/' + date_now + '/'
FINAL_GRAPH_PATH = OUTLINK_PATH + '/'
log_file = date_now + ".log"
network_graph = nx.DiGraph()


class WebCrawler:
    def __init__(self, base_url):

        self.url_queue = deque()
        self.count = 0
        self.url_queue.append(base_url)
        self.crawled = set()
        Path(PROJECT_PATH).mkdir(parents=True, exist_ok=True)
        Path(OUTLINK_PATH).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def valid_link(url):
        # check domain and extension return ''if invalid. return link if valid
        if any(word in BLACK_LIST for word in url):
            return False
        elif DOMAIN != get_domain_name(url):
            # Filter out bad domains
            return False
        else:
            # Link Valid
            return True

    def get_links(self, html, url):
        links = scrape_links(html)
        relevant_links = set()
        for link in links:
            a_tag_text = link['href']
            if not any(bad_links in a_tag_text for bad_links in ['tel', 'mailto', '#']):
                a_url = edit_url(link['href'], url)
                if self.valid_link(a_url):
                    if a_url not in self.crawled:
                        # Add to queue only if the link is not crawled
                        self.url_queue.append(a_url)
                    # This is to add nodes for graph
                    relevant_links.add(a_url)
        # After you get all relevant links from a page
        # Add nodes and outlinks from current node
        add_edges(url, relevant_links, network_graph)

    def run_scraper(self):
        while self.count < MAX_COUNT:
            target_link = self.url_queue.popleft().rstrip('/')
            if target_link not in self.crawled:
                response = connect_page(target_link)
                if response is not None:
                    if response.status_code == requests.codes.ok and \
                            'text/html' in response.headers['Content-Type'] and \
                            self.valid_link(response.url):
                        # Status code 200, html file and no EXTERNAL redirect
                        # also check if redirected file is going to same URL
                        # print("Success: writing to file:", self.count)
                        self.count += 1
                        print(self.count, "URL Scraping:", target_link)
                        if target_link == response.url.rstrip('/'):
                            self.crawled.add(target_link)
                        else:
                            self.crawled.add(target_link)
                            self.crawled.add(response.url.rstrip('/'))
                        self.get_links(response.text, response.url)
                        try:
                            write_data_to_file(
                                response.text, target_link, PROJECT_PATH + str(self.count))
                            logging.info(str(self.count) +
                                         ". URL Scraping: " + target_link)
                        except ValueError:
                            print("No data to parse in link ", target_link)
                            logging.error(
                                "No data to parse in link " + target_link)
                            self.count -= 1
                    else:
                        try:
                            print("Response Failed ", target_link,
                                  response.status_code)
                        except:
                            print("Response Failed ", target_link)
                        logging.error("Response Failed" + target_link)
        print("Max Reached")
        print("Generating Web Graph")
        # Retain only crawled sites in the graph
        save_graph(network_graph, OUTLINK_PATH + "final_graph.gpickle")
        # draw_graph(network_graph)


if __name__ == '__main__':
    logging.basicConfig(filename=log_file, level=logging.INFO)
    start = time.process_time()
    crawler = WebCrawler(BASE_URL)
    crawler.run_scraper()
    print("Time taken:", time.process_time() - start)
