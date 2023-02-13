import pandas as pd
import numpy as np
import os
import sys
import re
from degender_pronoun import degenderizer
from string import punctuation

alphabets= "([A-Za-z])"
prefixes = "(Mr|mr|St|Mrs|mrs|Ms|ms|Dr|dr|Prof|prof|Pro|pro)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever|Prof|Professor|Pro)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"
digits = "([0-9])"

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    if "..." in text: text = text.replace("...","<prd><prd><prd>")
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

def removeNer(full_name, first_name, last_name, text):      
    # remove name
    for name in [full_name, first_name, last_name]:
        if name:
            name = str(name)
            if len(name) > 1:
                for n in [name, name.lower(), name.upper(), name.title()]:
                    text = text.replace(n, "Person")
                    if not re.match('^[a-zA-Z]+$', n):
                        n = re.sub("[^a-zA-Z]", " ", n)
                        text = text.replace(n, "Person")
    return text

def apply_func(x):
    x['degender_comments'] = removeNer(x["professor_name"],x["first_name"],x["last_name"],x["comments"])
    return x

def lavenderize(D, text):
    """
        Takes an english text string and makes all pronouns gender neutral.
    """
    return D.degender(text)

def removeRepPunct(text):
    pattern = r"([{0}])[{0}]+".format(punctuation)
    return re.sub(pattern, r'\1 ', text)

root= sys.argv[1]
num = sys.argv[2]

with open(os.path.join(root, "stopwords.txt"),"r") as f:
    stopword_list = f.read().split("\n")
    
df = pd.read_csv(os.path.join(root,"sent_input_{}.csv".format(num)))
df['degender_comments'] = ""
df = df.apply(lambda x: apply_func(x), axis=1)
D = degenderizer()
df["degender_comments"] = (df["degender_comments"]
                            .apply(lambda x:removeRepPunct(x))
                            .apply(lambda x:lavenderize(D, x))
                            )
sentence_df = pd.DataFrame()
ind = df.index
for i in ind:
    x = df.loc[i,:]
    text = x["degender_comments"]
    sentences = split_into_sentences(text)
    for sentence in sentences:
        nr_non_stopword = len([word for word in sentence.split() if re.sub(r"[{0}]".format(punctuation), "", word.lower()) not in stopword_list])
        nr_word = sentence.count(" ") +1
        d = {"id":x["id"],"Unnamed: 0":x["Unnamed: 0"], "gender":x["gender"], "student_star":x["student_star"], "field":x["field"], "sentence":sentence}
        d1 = pd.DataFrame(d,index=[0])
        d1["nr_word"] = nr_word
        d1["nr_non_stopword"] = nr_non_stopword
        sentence_df = pd.concat([sentence_df,d1],ignore_index=True)

sentence_df.to_csv(os.path.join(root,"sent_output_{}.csv".format(num)),index=False)