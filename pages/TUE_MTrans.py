import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
df=pd.read_csv("assets/dataset.csv")
st.header("Dampak teknologi & transportasi terhadap tingkat obesitas")
st.subheader("Heatmap TUE & Mtrans")
st.write(df["NObeyesdad"].unique())
obeyes_map={
    "Insufficient_Weight": 0,
    "Normal_Weight":1,
    "Overweight_Level_I": 2,
    "Overweight_Level_II": 3,
    "Obesity_Type_I":4,
    "Obesity_Type_II": 5,
    "Obesity_Type_III":6
}
df["obeyes_map"]=df["NObeyesdad"].map(obeyes_map)
df["TUE_clean"]=df["TUE"].round().astype(int)
df_specified=df[["TUE_clean", "obeyes_map"]]
corr_mtx=df_specified.corr(method="pearson")
fig = px.imshow(
    corr_mtx,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    range_color=[-1,1],
    title="Korelasi Pearson"
)
st.plotly_chart(fig)
st.subheader("Dampak Teknologi & Transportasi")
tue_labels = {0: "0-2 Jam (Low)", 1: "3-5 Jam (Mid)", 2: ">5 Jam (High)"}
df["TUE_label"] = df["TUE_clean"].map(tue_labels)
fig_trans = px.box(
    df, 
    x="MTRANS", # Transportasi
    y="obeyes_map", # Level Obesitas (Numerik 0-6)
    # color="TUE_label", # Waktu penggunaan gadget (0, 1, 2)
    title="Hubungan Transportasi terhadap Tingkat Obesitas",
    labels={"NObeyesdad": "Tingkat Obesitas (0=Kurus, 6=Obesitas III)"}
)
st.plotly_chart(fig_trans)
fig_tech=px.box(
    df, 
    x="TUE_label", # Transportasi
    y="obeyes_map", # Level Obesitas (Numerik 0-6)
    # color="TUE_label", # Waktu penggunaan gadget (0, 1, 2)
    title="Hubungan Gadget terhadap Tingkat Obesitas",
    labels={"NObeyesdad": "Tingkat Obesitas (0=Kurus, 6=Obesitas III)"}
)
st.plotly_chart(fig_tech)