import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import seaborn as sns
from matplotlib.colors import LogNorm, Normalize
from adjustText import adjust_text
import pandas as pd
import numpy as np
import os
import matplotlib.ticker as tkr

root = r"your path"
def read_data(filename, rank, gender, filetype="cleaned_adjs"):
    df = pd.read_excel(os.path.join(root,filename), sheet_name=filetype).set_index('word')
    t = df[(df["rank"] == rank) & (df["gender"] == gender)]
    return t

colors = ["#F49980", "#539AC7"]

def prepare_data(rank, gender, wordtype):
    filename = r"top_30_dunning.xlsx"
    c = read_data(filename, rank, gender, filetype=wordtype)
    c["color"] = c["gender"].map({"female": colors[0], "male": colors[1]})
    c["logscore"] = np.log2(abs(c["score"]))
    return c

def plot_subsplot(ax, c, title, xlabel):
    scatters = ax.scatter(c["prof"], c["logscore"], c=c["color"], s=4**2)
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_ylabel(r"log$_{2}$(Dunning score)", fontsize=9)
    #stylize
    ax.set_ylim(bottom=c["logscore"].min()-0.7)
    loc = tkr.MultipleLocator(base=1.0) # this locator puts ticks at regular intervals
    ax.yaxis.set_major_locator(loc)
    ax.grid(color="black", alpha=0.2, ls="--")
    ax.set_title(title, fontsize=10, fontweight="bold")
    texts = [ax.text(x=c.loc[word,"prof"], y=c.loc[word,"logscore"], s=word,fontsize=8)
         for word in c.index]
    adjust_text(texts, ax=ax,
            expand_text=(1.01, 1.05), # narrow the gap between texts
            force_text=(0.7, 0.9), # make texts more sparse
            arrowprops=dict(arrowstyle='-|>', color="gray", alpha=0.3))
    
titles = {(0,0):"(A) Five-star reviews for women",
         (0,1):"(B) Five-star reviews for men",
         (1,0):"(C) One-star reviews for women",
         (1,1):"(D) One-star reviews for men",}
xlabels = {(0,0):"Popularity (% of women)",
         (0,1):"Popularity (% of men)",
         (1,0):"Popularity (% of women)",
         (1,1):"Popularity (% of men)",}
    
plt.style.use("seaborn-white")
# adj
fig, axes = plt.subplots(2,2,figsize=(8,8))
ranks = [5,1]
genders = ["female","male"]
wordtype="cleaned_adjs"
for i, rank in enumerate(ranks):
    for j, gender in enumerate(genders):
        c = prepare_data(rank, gender, wordtype)
        title = titles[(i,j)]
        xlabel = xlabels[(i,j)]
        plot_subsplot(axes[i][j], c, title, xlabel)

sns.despine()
plt.subplots_adjust(wspace=0.2,hspace=0.2)
fig.savefig("scatter_adj.pdf",dpi=300,bbox_inches="tight", pad_inches=0.1)

# non-adj
plt.style.use("seaborn-white")
fig, axes = plt.subplots(2,2,figsize=(8,8))
genders = ["female","male"]
wordtype="cleaned_noner"
for i, rank in enumerate(ranks):
    for j, gender in enumerate(genders):
        c = prepare_data(rank, gender, wordtype)
        title = titles[(i,j)]
        xlabel = xlabels[(i,j)]
        plot_subsplot(axes[i][j], c, title, xlabel)

sns.despine()
plt.subplots_adjust(wspace=0.2,hspace=0.2)
fig.savefig("scatter_word.pdf",dpi=300,bbox_inches="tight", pad_inches=0.1)
