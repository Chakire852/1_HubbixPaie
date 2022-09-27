import re
import nltk
import string
import pickle
import numpy as np
import pandas as pd
import gensim.downloader as api
from pandas.core.frame import DataFrame
from config.helper import read_config



from nltk import word_tokenize
from core.crud import updateClusterArticle
from api.endpoints.article import get_articles_from_document
from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics import silhouette_samples, silhouette_score

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Open or download Google pre-trained Word2Vec model
def getGoogleModel():
    config = read_config()
    modelpath = config['APPSettings']['modelpath']
    try:
        model = pickle.load(open(modelpath, 'rb'))
        print("Loading model from file")
    except:
        print("Downloading model from web")
        model = api.load('word2vec-google-news-300')
        pickle.dump(model, open(modelpath, 'wb'))
    return model

# Clean and Tokenize Data
def clean_text(text, tokenizer):
    """Pre-process text and generate tokens

    Args:
        text: Text to tokenize.

    Returns:
        Tokenized text.
    """
    text = str(text).lower()  # Lowercase words
    text = re.sub(r"\s+", " ", text)  # Remove multiple spaces in content
    text = re.sub(r"(?<=\w)-(?=\w)", " ", text)  # Replace dash between words
    text = re.sub(
        f"[{re.escape(string.punctuation)}]", "", text
    )  # Remove punctuation

    tokens = tokenizer(text, language='french')  # Get tokens from text
    return tokens

def vectorize(list_of_docs, model):
    """Generate vectors for list of documents using a Word Embedding

    Args:
        list_of_docs: List of documents
        model: Gensim's Word Embedding

    Returns:
        List of document vectors
    """
    features = []

    for tokens in list_of_docs:
        zero_vector = np.zeros(model.vector_size)
        vectors = []
        for token in tokens:
            if token in model:
                try:
                    vectors.append(model[token])
                except KeyError:
                    continue
        if vectors:
            vectors = np.asarray(vectors)
            avg_vec = vectors.mean(axis=0)
            features.append(avg_vec)
        else:
            features.append(zero_vector)
    return features

def mbkmeans_clusters(
	X, 
    k, 
    mb, 
    print_silhouette_values, 
):
    """Generate clusters and print Silhouette metrics using MBKmeans

    Args:
        X: Matrix of features.
        k: Number of clusters.
        mb: Size of mini-batches.
        print_silhouette_values: Print silhouette values per cluster.

    Returns:
        Trained clustering model and labels based on X.
    """
    km = MiniBatchKMeans(n_clusters=k, batch_size=mb).fit(X)
    print(f"For n_clusters = {k}")
    print(f"Silhouette coefficient: {silhouette_score(X, km.labels_):0.2f}")
    print(f"Inertia:{km.inertia_}")

    if print_silhouette_values:
        sample_silhouette_values = silhouette_samples(X, km.labels_)
        print(f"Silhouette values:")
        silhouette_values = []
        for i in range(k):
            cluster_silhouette_values = sample_silhouette_values[km.labels_ == i]
            silhouette_values.append(
                (
                    i,
                    cluster_silhouette_values.shape[0],
                    cluster_silhouette_values.mean(),
                    cluster_silhouette_values.min(),
                    cluster_silhouette_values.max(),
                )
            )
        silhouette_values = sorted(
            silhouette_values, key=lambda tup: tup[2], reverse=True
        )
        for s in silhouette_values:
            print(
                f"Cluster {s[0]}: Size:{s[1]} | Avg:{s[2]:.2f} | Min:{s[3]:.2f} | Max: {s[4]:.2f}"
            )
    return km, km.labels_

def clusterDocument(doc_id):
    
    print('Getting articles')
    listArticles = get_articles_from_document(doc_id)
    articles = pd.DataFrame(listArticles, columns=['Id', 'Name', 'Cid', 'Text', 'DocId', 'Cluster'])

    df = articles.copy()
    print('Pre-processing text')
    df['Text'] = df['Text'].astype(str)
    df['Tokens'] = df['Text'].map(lambda x: clean_text(x, word_tokenize))

    df = df[['Text', 'Tokens']]

    all_texts = df['Text'].values
    tokenized_texts = df['Tokens'].values

    print('Getting model')
    wv = getGoogleModel()

    print('Vectorizing')
    vectorized_texts = vectorize(tokenized_texts, model=wv)

    print('Clustering')
    clustering, cluster_labels = mbkmeans_clusters(
	    X = vectorized_texts,
        k = 2,
        mb = 500,
        print_silhouette_values=True,
    )

    print('Formatting results')
    df_clusters = pd.DataFrame({
        'Text': all_texts,
        'Tokens': [' '.join(text) for text in tokenized_texts],
        'Cluster': cluster_labels
    })

    articles['Cluster'] = df_clusters['Cluster'].values

    for index, row in articles.iterrows():
        updateClusterArticle(row['Id'], row['Cluster'])