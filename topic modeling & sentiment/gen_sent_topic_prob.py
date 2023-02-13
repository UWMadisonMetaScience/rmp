import pandas as pd
import os
import sys
from bertopic import BERTopic

root = sys.argv[1]
rank = sys.argv[2]
num = sys.argv[3]

# transform all sentences
filename1= os.path.join(root, "output_{0}_{1}.csv".format(rank,num))
filename2= os.path.join(root, "topic_model_merge_{0}".format(rank)) # bertopic trained model
to_transform = pd.read_csv(filename1)
topic_model = BERTopic.load(filename2)

sentences = to_transform["sentence"]
topics, probs = topic_model.transform(sentences)

prob_mat = pd.DataFrame(probs, columns = ["topic_"+str(i) for i in range(probs.shape[1])])
to_transform = pd.concat([to_transform, prob_mat], axis=1)

to_transform.to_csv(os.path.join(root, "tf_prob_output_{0}_{1}.csv".format(rank,num)),index=False)