import glob
import re
import string
import os
from pathlib import Path
import joblib
import nltk
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
from sklearn.metrics.pairwise import cosine_similarity
try:
    import cPickle as pickle
except:
    import pickle
spacy_nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])


lemmatizer = nltk.stem.WordNetLemmatizer()


def lemmatize_text(text_tokens):
    return [lemmatizer.lemmatize(w) for w in text_tokens]


# def tokenize(doc):
#     doc_1 = doc.translate(doc.maketrans('', "", string.punctuation))
#     word_tokens = nltk.word_tokenize(doc_1)
#     no_stop_doc = [w for w in word_tokens if w.isalpha()]
#     lemmatized_doc = lemmatize_text(no_stop_doc)
#     return no_stop_doc

def tokenize(doc):
    doc_1 = spacy_nlp(doc)
    no_stop_doc = [
        token.lemma_ for token in doc_1 if not token.is_stop and not token.is_punct]
    return no_stop_doc

def get_models():
    data_array = []
    currpath = Path(__file__).parent
    if not Path(currpath / 'DataFiles/dataFrame_bk.pkl').exists():
        print("File does not exist")
        files = glob.glob("./DataFiles/CrawledData/20200510/*")
        print(len(files))
        for file in files:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                data_array.append([re.sub('./DataFiles/CrawledData/20200510/', '', file),
                                re.sub(' +', ' ', f.read())])
        df = pd.DataFrame(data_array, columns=['File', 'Contents'])
        df = pd.DataFrame(data_array, columns=['File', 'Contents'])
        df['Link'] = df['Contents'].apply(lambda x: x.split("\n")[0])
        df['Doc'] = df['Contents'].apply(lambda x: x.split("\n")[1])
        df.to_pickle(currpath / 'DataFiles/dataFrame_bk.pkl')
    else:
        print("File does exist")
        df = pd.read_pickle(currpath / 'DataFiles/dataFrame_bk.pkl')


    if not Path((currpath / 'DataFiles/vectorizer.joblib')):
        print("vectorizing")
        vectorizer = TfidfVectorizer(tokenizer=tokenize,
                                    strip_accents='ascii',
                                    ngram_range=(1, 3),
                                    token_pattern=r'\b[a-zA-Z]{3,}\b',
                                    max_features=160000,
                                    sublinear_tf=True)
        joblib.dump(vectorizer, currpath / 'DataFiles/vectorizer.joblib')
    else:
        print("vector File does exist")
        vectorizer = joblib.load(currpath / 'DataFiles/vectorizer.joblib')


    if not Path((currpath / 'DataFiles/tfidf.joblib')):
        print("TFIDFs creating")
        tfidfs = vectorizer.fit_transform(df['Contents'])
        joblib.dump(tfidfs, currpath / 'DataFiles/tfidf.joblib')
    else:
        print("TFIDFs File does exist")
        tfidfs = joblib.load(currpath / 'DataFiles/tfidf.joblib')
    return (df, vectorizer, tfidfs)
    
    
