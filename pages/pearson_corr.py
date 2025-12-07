import streamlit as st
import pandas as pd
from scipy.stats import chi2_contingency
import numpy as np
import plotly.express as px
df_norm = pd.read_csv("assets/normalizedObesity.csv")
df_norm["BMI"]=df_norm["Weight"]/(df_norm["Height"]**2)
target_cols = [
    "Age", 
    "Height", 
    "Weight", 
    "FAVC",  
    "FAF",   
    "CH2O",  
    "FCVC", 
    "BMI"   
]
df_selected = df_norm[target_cols]
corr_matrix = df_selected.corr(method='pearson')
fig_corr = px.imshow(
    corr_matrix,
    text_auto=".2f",
    aspect="auto",
    color_continuous_scale="RdBu_r", 
    range_color=[-1, 1], 
    labels=dict(color="Koefisien Korelasi")
)

fig_corr.update_layout(
    title="Hubungan Pearson Antar Variabel",
    xaxis_title="Variabel",
    yaxis_title="Variabel",
    width=700,
    height=600
)

st.plotly_chart(fig_corr)