import glob
import pickle
from collections import Counter
from pathlib import Path
import networkx as nx

from Crawler.GenerateGraph import remove_nodes


def page_rank():
    currpath = Path(__file__).parent

    G = nx.read_gpickle(
        currpath / "Datafiles/Links/20200510/final_graph.gpickle")

    files = glob.glob(
        r"./DataFiles/CrawledData/20200510/*")

    print(len(files))
    links = []
    for i in files:
        with open(i, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            link = content.split('\n')[0]
            links.append(link)

    # Remove nodes that are not a part of the corpus
    remove_nodes(links, G)
    pageRank = Counter(nx.pagerank(G,
                                   alpha=0.85,
                                   weight='weight',
                                   max_iter=10))
    print(len(pageRank))
    with open(currpath / 'DataFiles/page_rank.pkl', 'wb') as f:
        pickle.dump(pageRank, f)
    return pageRank.most_common(50)
