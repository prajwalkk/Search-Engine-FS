import spacy
import joblib
import pickle
import nltk

import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from vectorizer_pipeline import tokenize
nltk.download('popular', quiet=True)
spacy_nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

currpath = Path(__file__).parent

RESULT_LIMIT = 10
QUERY_EXPN_LIMIT = 20
vectorizer = None
tfidfs = None
df = None
page_rank = None
init_val = 0

def initialize_objects():
    global vectorizer,tfidfs ,df ,page_rank ,init_val 
    vectorizer = joblib.load(currpath / 'DataFiles/vectorizer.joblib')
    tfidfs = joblib.load(currpath / 'DataFiles/tfidf.joblib')
    df = pd.read_pickle(currpath / 'DataFiles/dataFrame_bk.pkl')
    page_rank = pickle.load(open(currpath / 'DataFiles/page_rank.pkl', 'rb'))
    init_val = 1




def analyse_query(query, n=10, page_rank_flag=False):
    if(init_val == 0):
        return ["None"] * 5
    
    RESULT_LIMIT = int(n)
    print(query)
    q_tfidf = vectorizer.transform([query])
    print(q_tfidf.shape, tfidfs.shape)

    dict_cossim = {}
    for i in range(len(df)):
        int_dict = {}
        int_dict = {'Link': df.loc[i]['Link'],
                    'Content': df.loc[i]['Doc'],
                    'CosSim': cosine_similarity(tfidfs[i], q_tfidf),
                    'PageRank': page_rank[df.loc[i]['Link']]
                    }
        dict_cossim[i] = int_dict
    cosine_similarity(tfidfs[0], q_tfidf)

    top_n = sorted(dict_cossim.keys(),
                   key=lambda x: dict_cossim[x]['CosSim'][0],
                   reverse=True)[:RESULT_LIMIT]

    top_n_page_rank = sorted(dict_cossim.keys(),
                             key=lambda x: (
        ( dict_cossim[x]['CosSim'][0]) + (dict_cossim[x]['PageRank'])),
        reverse=True)[:RESULT_LIMIT]

    link_list = []
    doc_list = []
    cossim_list = []
    pagerank_list = []

    if not page_rank_flag:
        print("Cosssim")
        for i in top_n:
            #print(dict_cossim[i]['Link'], dict_cossim[i]['CosSim'][0])
            link_list.append(dict_cossim[i]['Link'])
            doc_list.append(dict_cossim[i]['Content'])
            cossim_list.append(dict_cossim[i]['CosSim'])
            pagerank_list.append(dict_cossim[i]['PageRank'])

    elif page_rank_flag:
        print("Page Rank")
        for i in top_n_page_rank:
            link_list.append(dict_cossim[i]['Link'])
            doc_list.append(dict_cossim[i]['Content'])
            cossim_list.append(dict_cossim[i]['CosSim'])
            pagerank_list.append(dict_cossim[i]['PageRank'])

    # Calculating the Query terms to expand
    relevant_docs_sum = np.sum(tfidfs[top_n], axis=0)
    irrelevant = np.subtract(np.sum(tfidfs, axis=0),
                             relevant_docs_sum)
    alpha, beta, gamma = 1, 0.75, 0.15
    nr, d_nr = (10, tfidfs.shape[0] - 10)
    query_m = q_tfidf + (beta * relevant_docs_sum / nr) - \
        (gamma * irrelevant / d_nr)
    yy = np.asarray(query_m).flatten()
    indices = np.argpartition(yy, -20)[-20:]
    sortedindices = indices[np.argsort(yy[indices])][::-1]

    features = vectorizer.get_feature_names()
    queries_terms = [features[i]
                     for i in sortedindices if features[i] not in query]

    def filter_query_terms(query_list):
        # Try to get non repeated queries. Example:,
        # Ignores "list" if "list index" is present in the array
        result = []
        for q in query_list:
            if not any([q in res for res in query_list if q != res]):
                result.append(q)
        return result

    res_filtered = filter_query_terms(queries_terms)

    final_qe_terms = []
    # Attach results to the query searched
    # this is discarded as it causes results to be skewed
    for i in res_filtered:
        qexpand = query.split() + i.split()
        final_qe_terms.append(
            " " .join(sorted(set(qexpand), key=qexpand.index)))

    print(link_list)
    print(queries_terms)

    return (link_list, doc_list, cossim_list, pagerank_list, res_filtered)
