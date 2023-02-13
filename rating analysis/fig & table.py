import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.ticker as plticker
from nltk.corpus import stopwords
from scipy.stats import mannwhitneyu

root = r"your path"
df = pd.read_csv(os.path.join(root, r"data.csv"))

genders = ["male","female"]
fields = [
"Applied Sciences",
"Natural Sciences",
"Math & Computing",
"Engineering",
"Medicine Health",
"Social Sciences",
"Education",
"Humanities",
]

# Table 2. Average word counts of text comments per review by field and gender
df5 = df.loc[df["gender"].isin(genders) & (df["student_star"]==5), :]
df1 = df.loc[df["gender"].isin(genders) & (df["student_star"]==1), :]

## mann test
def mann_test(df, value="word_comment", field=None):
    if field:
        f = df.loc[(df["gender"] == "female") & (df["field"] == field), value].dropna()
        m = df.loc[(df["gender"] == "male") & (df["field"] == field), value].dropna()
    else:
        f = df.loc[(df["gender"] == "female"), value].dropna()
        m = df.loc[(df["gender"] == "male"), value].dropna()
    return mannwhitneyu(f,m)

def gen_table(df, value="word_comment"):
    table = (pd.pivot_table(df, index="field", columns="gender", values=value, aggfunc=np.mean)
            .reindex(fields)
            .reset_index()
            )
    table["diff"] = table["female"] - table["male"]
    table = table.applymap(lambda x: round(x, 2) if isinstance(x, float) else x)
    table["p-value"] = table["field"].apply(lambda x: round(mann_test(df, value, field=x)[1], 3))
    return table

print(pd.pivot_table(df1, index="gender", values="word_comment", aggfunc=np.mean))
print(mann_test(df1, value="word_comment", field=None))
gen_table(df1, value="word_comment")
print(pd.pivot_table(df5, index="gender", values="word_comment", aggfunc=np.mean))
print(mann_test(df5, value="word_comment", field=None))
gen_table(df5, value="word_comment")

# Table 3. Distributions of five- and one-star review numbers and percentages by professor gender and field
res = []
for rank in [1,5]:
    for gender in genders:
        print(rank, gender)
        base_df = df.loc[(df["student_star"]==rank) & (df["gender"] == gender) & (df["field"].isin(fields))]
        pt_com = pd.pivot_table(base_df, index = "field", values="Unnamed: 0", aggfunc=lambda x: x.nunique())
        pt_prof =pd.pivot_table(base_df, index = "field", values="id", aggfunc=lambda x: x.nunique())
        
        all_df = df.loc[(df["gender"] == gender) & (df["field"].isin(fields))]
        all_pt_com = pd.pivot_table(all_df, index = "field", values="Unnamed: 0", aggfunc=lambda x: x.nunique())
        all_pt_prof =pd.pivot_table(all_df, index = "field", values="id", aggfunc=lambda x: x.nunique())
        pt_com_perc = pt_com/all_pt_com*100
        pt_prof_perc = pt_prof/all_pt_prof*100
        
        pt = pd.concat([pt_com, pt_com_perc, pt_prof, pt_prof_perc], axis=1)
        pt.columns = pd.MultiIndex.from_tuples([(rank, "Review",gender,"#"),
                                                (rank, "Review",gender,"%"),
                                                (rank, "Professor",gender,"#"),
                                                (rank, "Professor",gender,"%")])
        res.append(pt)
res_df = pd.concat(res, axis=1)

res2 = []
for rank in [1,5]:
    for gender in genders:
        print(rank, gender)
        base_df = df.loc[(df["student_star"]==rank) & (df["gender"] == gender) & (df["field"].isin(fields))]
        pt_com = base_df["Unnamed: 0"].nunique()
        pt_prof = base_df["id"].nunique()
        
        all_df = df.loc[(df["gender"] == gender) & (df["field"].isin(fields))]
        all_pt_com = all_df["Unnamed: 0"].nunique()
        all_pt_prof = all_df["id"].nunique()
        pt_com_perc = pt_com/all_pt_com*100
        pt_prof_perc = pt_prof/all_pt_prof*100
        
        pt = pd.DataFrame([[pt_com, pt_com_perc, pt_prof, pt_prof_perc]], index=["All"])
        pt.columns = pd.MultiIndex.from_tuples([(rank, "Review",gender,"#"),
                                                (rank, "Review",gender,"%"),
                                                (rank, "Professor",gender,"#"),
                                                (rank, "Professor",gender,"%")])
        res2.append(pt)
        
res2_df = pd.concat(res2, axis=1)
print(pd.concat([res_df,res2_df]).sort_index(axis=1, level=[0,1]))

# Fig 3. Professors’ percentage across the numbers of received reviews by professor gender and field
genders = ["male","female"]
df1 = df.loc[df["gender"].isin(genders) & (df["student_star"]==1)]
base1 = df1.groupby(["id", "gender"])["Unnamed: 0"].nunique().reset_index()
df5 = df.loc[df["gender"].isin(genders) & (df["student_star"]==5)]
base5 = df5.groupby(["id", "gender"])["Unnamed: 0"].nunique().reset_index()

ma1 = base1[base1["gender"]=="male"].groupby(["Unnamed: 0"])["id"].nunique()
m_norm1 = ma1/ ma1.sum() * 100
fa1 = base1[base1["gender"]=="female"].groupby(["Unnamed: 0"])["id"].nunique()
f_norm1 = fa1/ fa1.sum() * 100

ma5 = base5[base5["gender"]=="male"].groupby(["Unnamed: 0"])["id"].nunique()
m_norm5 = ma5/ ma5.sum() * 100
fa5 = base5[base5["gender"]=="female"].groupby(["Unnamed: 0"])["id"].nunique()
f_norm5 = fa5/ fa5.sum() * 100

plt.style.use("seaborn-white")
colors = ["#F38E72", "#408FC1"]
fig, axes = plt.subplots(1,2, figsize=(8,3))

ax = axes[0]
ax.plot(f_norm5.index, f_norm5.values, color=colors[0], label="Women", linewidth=3)
ax.plot(m_norm5.index, m_norm5.values, color=colors[1], label="Men")
ax.set_xlabel("# of received reviews")
ax.set_ylabel(r"% of professors")
loc = plticker.MultipleLocator(base=10.0)
ax.yaxis.set_major_locator(loc)
ax.grid(axis="both", ls="--")

ax.set_title("Five-star reviews")
ax.legend()
ax.set_xlim(right=53)
ax.set_ylim(top=43)
sns.despine()
ax.text(x=-0.06, y=1.02, s="(A)", fontweight="bold", transform=ax.transAxes)

ax = axes[1]
ax.plot(f_norm1.index, f_norm1.values, color=colors[0], label="Women", linewidth=3)
ax.plot(m_norm1.index, m_norm1.values, color=colors[1], label="Men")
ax.set_xlabel("# of received reviews")
ax.set_ylabel(r"% of professors")
ax.yaxis.set_major_locator(loc)
ax.grid(axis="both", ls="--")
ax.set_title("One-star reviews")
ax.legend()
ax.set_xlim(right=53)
ax.set_ylim(top=43)
sns.despine()
ax.text(x=-0.06, y=1.02, s="(B)", fontweight="bold", transform=ax.transAxes)

fig.savefig(r"review_dist.jpg", dpi=300, bbox_inches="tight", pad_inches=0.1)
fig.savefig(r"review_dist.pdf", dpi=300, bbox_inches="tight", pad_inches=0.1)
plt.show()

# Fig 4. Rating distributions and means of by professor gender and field
plt.style.use("seaborn-white")
colors = ["#F38E72", "#408FC1"]

def prepare_data(t):
    t1 = t.copy()
    t1["field"] = "All"
    return pd.concat([t1, t])

def plot_violin_mean(ax,
                     t,
                     ylabel,
                     isLengend=False,
                     ):
    g=sns.violinplot(data=t,
                x="field",
                y="student_star",
                hue="gender",
                hue_order=genders,
                split=True,
                inner=None,
                ax=ax,
                palette=colors,
                order=fields,
                saturation=1,
            )

    # plot mean as bars
    for i, gender in enumerate(genders):
        means = t[t["gender"]==gender].groupby(["field"])["student_star"].mean()
        means = means.reindex(fields)
        print(means)
        ax.errorbar(x=range(len(fields)),
                y=means,
                xerr=0.3,
                ecolor=colors[i],
                elinewidth=2,
                ls='none',
                capsize=5
                )
    
    ax.set_xticklabels(fields, ha='right', rotation=20)
    ax.set_xlabel(None)
    # ax.set_ylim(top=top)
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", ls="--")
    g.legend_.set_title(None)
    g.legend_.remove()
    sns.despine()

fig, ax = plt.subplots(1,1, figsize=(8,4))
t = prepare_data(df)
plot_violin_mean(ax,
                     t,
                     ylabel=r"Rating",
                     )
#ax.patch.set_alpha(0.0) # make bg color transparent
leg_texts = ["Women", "Men"]
legend_elements = [Line2D([0], [0], marker='o', color='w', label=leg_texts[c].title(),markerfacecolor=color, markersize=10)
                for c,color in enumerate(colors)]
ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)
plt.show()
fig.savefig("violin_rating.pdf",dpi=300,bbox_inches="tight", pad_inches=0.0)
