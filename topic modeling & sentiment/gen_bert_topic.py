import pandas as pd
import os
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
import pickle
import sys
from umap import UMAP

def gen_topic_model(sentences, root, rank, stopword_list):
    vectorizer_model = CountVectorizer(ngram_range=(1, 2),
                                       stop_words=stopword_list,
                                       min_df=5)
    sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
    # embeddings = sentence_model.encode(sentences, show_progress_bar=True)
    # with open(os.path.join(root, "embeddings_{}.pkl".format(rank)), "wb")  as output_file:
    #     pickle.dump(embeddings, output_file)
    # print("embeddings dumped")
    with open(os.path.join(root, r"embeddings_{}.pkl".format(rank)), "rb")  as output_file:
        embeddings = pickle.load(output_file)
    print("embeddings loaded")
    
    umap_model = UMAP(n_neighbors=15, n_components=5, 
                  min_dist=0.0, metric='cosine', random_state=666)
    topic_model = BERTopic(language="english",
                           min_topic_size=int(len(sentences)/1000),
                           umap_model=umap_model,
                           embedding_model=sentence_model,
                           vectorizer_model=vectorizer_model,
                           low_memory=False,
                           calculate_probabilities=True,
                           diversity=0.2).fit(sentences, embeddings)
        
    topic_model.save(os.path.join(root, "topic_bert_{0}".format(rank)))

def main(root, rank, stopword_list):
    try:
        filename = "sentence_df_{0}.csv".format(rank)
        df = pd.read_csv(os.path.join(root, filename))
        sentences = df["sentence"].to_list()
        print("start training")
        gen_topic_model(sentences,root, rank,stopword_list)
        print("finished")
    
    except Exception as e:
        print(e)
        

root= sys.argv[1]
rank = sys.argv[2]

with open(os.path.join(root, "stopwords.txt"),"r") as f:
    stopword_list = f.read().split("\n")

main(root, rank, stopword_list)