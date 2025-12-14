import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("./assets/cleanedDataset.csv")

counts = df.groupby(["CH2O", "NObeyesdad"], as_index=False).size()
counts["prop"] = counts.groupby("CH2O")["size"].transform(lambda x: x / x.sum())
st.dataframe(counts)


fig = px.bar(
    counts,
    x="CH2O",
    y="prop",
    color="NObeyesdad",  # Each transport type gets a color
    text=[
        f"{(i * 100):.2f}%" for i in counts["prop"]
    ],  # Optional: display counts on bars
    title="Distribution of Transportation by BMI",
    barmode="group",  # Stack bars; use 'group' for side-by-side
    category_orders={
        "NObeyesdad": [
            "Insufficient_Weight",
            "Normal_Weight",
            "Overweight_Level_I",
            "Overweight_Level_II",
            "Obesity_Level_I",
            "Obesity_Level_II",
            "Obesity_Level_III",
        ]
    },
)

fig.update_layout(
    xaxis_title="BMI Category",
    yaxis_title="Number of People",
    bargap=0.05,
    bargroupgap=0.001,
)


st.plotly_chart(fig)
