import pandas as pd
import os
import sys
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
from scipy.special import softmax

MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)

# PT
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

def pred_sentiment(text):
    encoded_input = tokenizer(str(text), return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    return scores[0], scores[1], scores[2]

root = sys.argv[1]
rank = sys.argv[2]
num = sys.argv[3]

df = pd.read_csv(os.path.join(root,"tf_sent_output_{}_{}.csv".format(rank,num)))
df["neg"], df["neu"], df["pos"]= zip(*df["sentence"].apply(lambda x: pred_sentiment(x)))
df.to_csv(os.path.join(root,"flair_output_{}_{}.csv".format(rank,num)))