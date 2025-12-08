import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
df=pd.read_csv("assets/normalizedObesity.csv")
df_specific=df[["NCP", "FAF", "FCVC", "CH2O", "TUE", "Gender", "CALC","MTRANS","BMI"]]
# correlation matrix
corr_mtx=df_specific.corr(method="pearson")
fig_corr=px.imshow(
    corr_mtx,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    range_color=[-1,1],
    title="Korelasi Pearson"
)
st.plotly_chart(fig_corr)
