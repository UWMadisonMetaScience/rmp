import pandas as pd
import contractions
from collections import Counter
import re
import string
from gender_detector import gender_detector as gd
detector = gd.GenderDetector('us')

df = pd.read_csv('RMP_big_data with online course.csv')
df['professor_name'] = [x.replace('\\','') for x in df['professor_name'].values.tolist() ]
df['professor_name'] = [re.sub(' +', ' ',x) for x in df['professor_name'].values.tolist() ]
last_name = []
first_name = []
first_middle_name = []
for name in [' '.join(['' if idx.lower() in ['dr.','proff','proff.', 'dr','prof.','prof','eng','eng.','mr.','ms.','mr','ms','mrs','mrs.'] else idx for idx in x.split()]) for x in df['professor_name'].values.tolist() ]:
    if len(name.split()) > 1:
        first_name.append(name.split()[0])
        first_middle_name.append(' '.join(name.split()[:-1]))
        last_name.append(name.split()[-1])
    else:
        first_name.append(name.split()[0])
        first_middle_name.append(name.split()[0])
        last_name.append('')    
for x in range(5000):
    if len(first_middle_name[x]) <2:
        first_middle_name[x] = first_middle_name[x] + ' ' + last_name[x]
        last_name[x] = ''
df ['first_name'] = first_name
df ['last_name'] = last_name
df['first_middle_name'] = first_middle_name

# Apply method 1
f_pronouns = []
m_pronouns = []
gender1 = []
df['comments'] = df['comments'].fillna("")
for comment in df['comments'].values.tolist():
    comment = contractions.fix(comment.replace('\\',''))
    comment = comment.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation))).lower()
    words = comment.split()
    f_pronouns = (sum(1 for x in words if x in ['she','her','herself','hers','mrs','ms'] ))
    m_pronouns = (sum(1 for x in words if x in ['he','him','himself','his','mr'] ))
    if (f_pronouns == 0 and m_pronouns == 0):
        gender1.append('')
    elif (f_pronouns == 0):
        gender1.append('male')
    elif (m_pronouns == 0):
        gender1.append('female')
    elif (f_pronouns/m_pronouns >= 3):
        gender1.append('female')
    elif (m_pronouns/f_pronouns >= 3):
        gender1.append('male')
    else:
        gender1.append('')
        
for x in range(len(gender1)):
    if gender1[x] == '':
        idx = df.loc[df.professor_name==df.loc[x,'professor_name']].index.values.tolist() 
        tp = list(map(gender1.__getitem__, idx))
        if tp != []:
            gender1[x] = Counter(tp).most_common(1)[0][0]

# Apply method 2
gender2 = []
for name in df['first_name'].values.tolist():
    try:
        if (detector.guess(name) == 'unknown'):
            gender2.append('')
        else:
            gender2.append(detector.guess(name))
    except: 
        gender2.append('')
        
for x in range(5000):
    if df.loc[x,'professor_name'].split()[0].lower() in ['mr.','mr']:
        gender2[x] == 'male'
    elif df.loc[x,'professor_name'].split()[0].lower() in ['ms.','ms','mrs','mrs.']:
        gender2[x] == 'female'

# apply method 3
df2 = pd.read_csv('vincent_gender_firstName.csv') # see doi:10.1038/504211a
df2 = df2.query('country in ["Canada","United States"]').reset_index(drop=True)
df2.fillna('',inplace=True)
gender3 = []
for name in df['first_middle_name'].values.tolist():
    indices = [i for i, x in enumerate(df2['givenname'].values.tolist()) if x == name]
    gender = [df2.loc[x,'gender'] for x in indices ]
    if len(gender) == 0:
        gender3.append('')
    elif len(Counter(gender).keys()) == 1:
        gender3.append(list(Counter(gender).keys())[0])
    else :
        gender3.append(list(Counter(gender).most_common(1)[0][0])[0])  

rename = {
        'M': 'male',
        'F': 'female',
        '': '',
        'UNI': '',
        'UNK': '',
        'INI': ''  }
gender3 = [rename.get(x,x) for x in gender3]

# combine results
gender = []
for x in range(len(df)):
    temp = [gender2[x],gender1[x],gender3[x]]
    if (gender1[x] != ''):
        gender.append(gender1[x])
    elif (gender2[x] == gender3[x]):
        gender.append(gender2[x])
    else: 
        gender.append('')