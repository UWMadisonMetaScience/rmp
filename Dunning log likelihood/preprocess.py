import pandas as pd
import re
import nltk
import pycld2 as cld2
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from flair.models import TARSTagger
from flair.data import Sentence
import pandas as pd

df = pd.read_pickle('data.pkl')

# language detection
language = []
for x in range(len(df)):
    _, _, _, detected_language = cld2.detect(df.loc[x,'comments'], returnVectors=True)
    language.append([y[2] for y in detected_language])
df['language'] = language


# Filtering languages (Taking out multiples language and single language other than english)
idx = [x for x in range(len(df)) if len(df.loc[x,'language'])!=1]
idx2 = [x for x in range(len(df)) if len(df.loc[x,'language'])==1 and df.loc[x,'language'][0] != 'ENGLISH' and df.loc[x,'language'][0] != 'Unknown']
idx = idx+idx2
df.loc[idx,['clean_comments','language']]

# removing named entities (University and names )from comments 
tars = TARSTagger.load('tars-ner')
labels = ['Person','University']
tars.add_and_switch_to_new_task('task 1', labels, label_type='ner')
no_ner = []
for comment in df.clean_comments.values.tolist():
    sentence = Sentence(' '.join(comment))
    tars.predict(sentence)
    temp = sentence.to_tagged_string("ner").split(' ')
    ind = [i for i, item in enumerate(temp) if re.search('<[A-Z]-Person>|<[A-Z]-University>', item)]
    ind += [y-1 for y in ind]
    for index in sorted(ind, reverse=True):
        del temp[index]
    no_ner.append(' '.join(temp))
df['no_ner'] = no_ner