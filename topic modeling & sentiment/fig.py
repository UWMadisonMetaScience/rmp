import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import os
import numpy as np
from ipywidgets import widgets
from ipywidgets.embed import embed_minimal_html

root = r"your path"

# data processing

data = pd.read_excel(os.path.join(root, "data1.xlsx"))
dfmap = pd.read_excel(os.path.join(root, "topic_mapping1.xlsx"))
df1 = pd.merge(data, dfmap, on="topic")

data = pd.read_excel(os.path.join(root, "data5.xlsx"))
dfmap = pd.read_excel(os.path.join(root, "topic_mapping5.xlsx"))
df5 = pd.merge(data, dfmap, on="topic")

df1["name"] = df1["name"].str.replace("_", "; ")
df5["name"] = df5["name"].str.replace("_", "; ")

# topic regression

# category order params
cat_orders = ["Overall", "Teaching", "Personal", "Material",
              "Structure", "Evaluation", "Grading"]

# color param
colors = ["#F38E72", "#408FC1"]

# Initialize figure
t1 = df1[(df1["pval"] < 0.05) & (df1["field"] == "All")
         & (df1["type"] == "topic")]
t5 = df5[(df5["pval"] < 0.05) & (df5["field"] == "All")
         & (df5["type"] == "topic")]
row_heights = [max(len(t1[t1["category"] == x]), len(
    t5[t5["category"] == x])) for x in cat_orders]
fig = make_subplots(rows=len(cat_orders),
                    cols=2,
                    row_heights=row_heights,
                    horizontal_spacing=0.02,
                    vertical_spacing=0.04,
                    # repeat subplot title
                    subplot_titles=[x for x in cat_orders for _ in range(2)]
                    )

# Add Traces
# first is topic
for i, t in enumerate([t5, t1]):
    for c, cat in enumerate(cat_orders):
        dfx = (t[(t["category"] == cat)]
               .sort_values("coef", ascending=True))
        subdf = dfx[(dfx["coef"] <= 0)]
        padding = row_heights[c] - len(dfx)  # padding the y axis
        fig.add_trace(go.Scatter(x=[None] * padding + subdf["coef"].tolist(),
                                 # avoid duplicate padding
                                 y=[" " * p for p in range(padding)] + \
                                 subdf["name"].tolist(),
                                 marker=dict(color=colors[1]),
                                 mode="markers",
                                 name=cat,
                                 legendgroup="Men",
                                 error_x=dict(type="data",
                                              symmetric=False,
                                              array=[None] * padding + (subdf["high"] -
                                                                        subdf["coef"]).tolist(),
                                              arrayminus=[None] * padding + (subdf["coef"] -
                                                                             subdf["low"]).tolist(),
                                              color=colors[1]
                                              ),
                                 ),
                      row=c+1,
                      col=i+1,
                      )

        subdf = dfx[(dfx["coef"] > 0)]
        fig.add_trace(go.Scatter(x=subdf["coef"],
                                 # no padding here cuz it's upper half
                                 y=subdf["name"],
                                 marker=dict(color=colors[0]),
                                 mode="markers",
                                 name=cat,
                                 legendgroup="Women",
                                 error_x=dict(type="data",
                                              symmetric=False,
                                              array=subdf["high"] -
                                              subdf["coef"],
                                              arrayminus=subdf["coef"] -
                                              subdf["low"],
                                              color=colors[0]
                                              ),
                                 ),
                      row=c+1,
                      col=i+1,
                      )

fig.update_layout(height=1500,
                  width=1000,
                  template="simple_white",
                  font=dict(family="Arial"),
                  showlegend=False,
                  margin=dict(t=80, b=80),
                  )

fig.add_annotation(
    x=.2,
    y=1.04,
    xref="paper",
    yref="paper",
    xanchor="center",
    text="<b>(A) Five-star reviews<b>",
    showarrow=False,
    font=dict(color="black",
              size=16,
              )
)

fig.add_annotation(
    x=0.5,
    y=1.04,
    xref="paper",
    yref="paper",
    xanchor="left",
    text="<b>(B) One-star reviews<b>",
    showarrow=False,
    font=dict(color="black",
              size=16,
              )
)

fig.update_xaxes(showgrid=True,
                 zeroline=True,
                 zerolinecolor="gray",
                 mirror=True,
                 )

fig.update_yaxes(type='category',
                 showgrid=True,
                 ticklabelstep=1,
                 mirror=True,
                 )

# move right subplots' y axes to the right
for c in range(len(cat_orders)):
    fig.update_yaxes(side="right",
                     col=2,
                     row=c + 1
                     )

# show x axis label at bottom
for col in [1, 2]:
    fig.update_xaxes(title=dict(text="Coefficient (women-men)",
                                standoff=0.01,
                                font_size=13),
                     ticklabelposition="outside",
                     col=col,
                     row=7
                     )

# draw legend
d1, d2 = 0.02, 0.006
x0, y0 = -0.2, -0.04
fig.add_shape(type="circle",
              xref="paper", yref="paper",
              x0=x0, y0=y0,
              x1=x0+d1, y1=y0+d2,
              opacity=1,
              fillcolor=colors[0],
              line_color=colors[0],
              )

fig.add_annotation(
    x=x0 + d1,
    y=y0 + d2 / 2,
    xref="paper",
    yref="paper",
    xanchor="left",
    yanchor="middle",
    text="Positive coefficient (higher probability for women)",
    showarrow=False,
    font=dict(color="black",
              size=12,
              )
)

x0, y0 = 0.6, -0.04
fig.add_shape(type="circle",
              xref="paper", yref="paper",
              x0=x0, y0=y0,
              x1=x0+d1, y1=y0+d2,
              opacity=1,
              fillcolor=colors[1],
              line_color=colors[1],
              )

fig.add_annotation(
    x=x0 + d1,
    y=y0 + d2 / 2,
    xref="paper",
    yref="paper",
    xanchor="left",
    yanchor="middle",
    text="Negative coefficient (higher probability for men)",
    showarrow=False,
    font=dict(color="black",
              size=12,
              )
)

fig.show()
fig.write_image(r"topic.pdf")

# sentiment regression

# category order params
cat_orders = ["Overall", "Teaching", "Personal", "Material",
              "Structure", "Evaluation", "Grading"]

# color param
colors = ["#F38E72", "#408FC1"]

# Initialize figure
t1 = df1[(df1["pval"] < 0.05) & (df1["field"] == "All")
         & (df1["type"] == "sent")]
t5 = df5[(df5["pval"] < 0.05) & (df5["field"] == "All")
         & (df5["type"] == "sent")]
row_heights = [max(len(t1[t1["category"] == x]), len(
    t5[t5["category"] == x])) for x in cat_orders]
fig = make_subplots(rows=len(cat_orders),
                    cols=2,
                    row_heights=row_heights,
                    horizontal_spacing=0.03,
                    vertical_spacing=0.04,
                    # repeat subplot title
                    subplot_titles=[x for x in cat_orders for _ in range(2)]
                    )

# Add Traces
# first is topic
for i, t in enumerate([t5, t1]):
    for c, cat in enumerate(cat_orders):
        dfx = (t[(t["category"] == cat)]
               .sort_values("coef", ascending=True))
        subdf = dfx[(dfx["coef"] <= 0)]
        padding = row_heights[c] - len(dfx)  # padding the y axis
        fig.add_trace(go.Scatter(x=[None] * padding + subdf["coef"].tolist(),
                                 # avoid duplicate padding
                                 y=[" " * p for p in range(padding)] + \
                                 subdf["name"].tolist(),
                                 marker=dict(color=colors[1]),
                                 mode="markers",
                                 name=cat,
                                 legendgroup="Men",
                                 error_x=dict(type="data",
                                              symmetric=False,
                                              array=[None] * padding + (subdf["high"] -
                                                                        subdf["coef"]).tolist(),
                                              arrayminus=[None] * padding + (subdf["coef"] -
                                                                             subdf["low"]).tolist(),
                                              color=colors[1]
                                              ),
                                 ),
                      row=c+1,
                      col=i+1,
                      )

        subdf = dfx[(dfx["coef"] > 0)]
        fig.add_trace(go.Scatter(x=subdf["coef"],
                                 # no padding
                                 y=subdf["name"],
                                 marker=dict(color=colors[0]),
                                 mode="markers",
                                 name=cat,
                                 legendgroup="Women",
                                 error_x=dict(type="data",
                                              symmetric=False,
                                              array=subdf["high"] -
                                              subdf["coef"],
                                              arrayminus=subdf["coef"] -
                                              subdf["low"],
                                              color=colors[0]
                                              ),
                                 ),
                      row=c+1,
                      col=i+1,
                      )

fig.update_layout(height=1500,
                  width=1000,
                  template="simple_white",
                  font=dict(family="Arial"),
                  showlegend=False,
                  margin=dict(t=80, b=80),
                  )

fig.add_annotation(
    x=0.2,
    y=1.04,
    xref="paper",
    yref="paper",
    xanchor="center",
    text="<b>(A) Five-star reviews<b>",
    showarrow=False,
    font=dict(color="black",
              size=16,
              )
)

fig.add_annotation(
    x=0.5,
    y=1.04,
    xref="paper",
    yref="paper",
    xanchor="left",
    text="<b>(B) One-star reviews<b>",
    showarrow=False,
    font=dict(color="black",
              size=16,
              )
)

fig.update_xaxes(showgrid=True,
                 zeroline=True,
                 zerolinecolor="gray",
                 mirror=True,
                 )

fig.update_yaxes(type='category',
                 showgrid=True,
                 ticklabelstep=1,
                 mirror=True,
                 )

# move right subplots' y axes to the right
for c in range(len(cat_orders)):
    fig.update_yaxes(side="right",
                     col=2,
                     row=c + 1
                     )

# show x axis label at bottom
for col in [1, 2]:
    fig.update_xaxes(title=dict(text="Coefficient (women-men)",
                                standoff=0.01,
                                font_size=13),
                     ticklabelposition="outside",
                     col=col,
                     row=7
                     )

# draw legend
d1, d2 = 0.02, 0.006
x0, y0 = -.2, -0.05
fig.add_shape(type="circle",
              xref="paper", yref="paper",
              x0=x0, y0=y0,
              x1=x0+d1, y1=y0+d2,
              opacity=1,
              fillcolor=colors[0],
              line_color=colors[0],
              )

fig.add_annotation(
    x=x0 + d1,
    y=y0 + d2 / 2,
    xref="paper",
    yref="paper",
    xanchor="left",
    yanchor="middle",
    text="Positive coefficient (stronger sentiment for women)",
    showarrow=False,
    font=dict(color="black",
              size=12,
              )
)

x0, y0 = .6, -0.05
fig.add_shape(type="circle",
              xref="paper", yref="paper",
              x0=x0, y0=y0,
              x1=x0+d1, y1=y0+d2,
              opacity=1,
              fillcolor=colors[1],
              line_color=colors[1],
              )

fig.add_annotation(
    x=x0 + d1,
    y=y0 + d2 / 2,
    xref="paper",
    yref="paper",
    xanchor="left",
    yanchor="middle",
    text="Negative coefficient (stronger sentiment for men)",
    showarrow=False,
    font=dict(color="black",
              size=12,
              )
)

fig.show()
fig.write_image(r"sent.pdf")
