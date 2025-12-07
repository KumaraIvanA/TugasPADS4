import streamlit as st
import pandas as pd
from scipy.stats import chi2_contingency
import numpy as np
import plotly.express as px
st.set_page_config(page_title="analisis pencegahan obesitas", layout="wide")
st.title("dashboard visualisasi insight")
@st.cache_data
def load_data():
    try:
        df=pd.read_csv("assets\dataset.csv", sep=",")
    except:
        df=pd.read_csv("assets\dataset.csv", sep=";")
    return df
df=load_data()
ncp_map={
    1: "One",
    2: "Two",
    3: "Three",
    4: "More than three"
}
df["NCP"] = pd.to_numeric(df["NCP"], errors="coerce")  
df["NCP"]=np.floor(df["NCP"].astype(int))
df["NCP_num"]=df["NCP"].map(ncp_map)
order_ncp = ["One","Two", "Three", "More than three"]

df["NCP_num"] = pd.Categorical(
    df["NCP_num"],
    categories=order_ncp,
    ordered=True
)
df["BMI"]=df["Weight"]/(df["Height"]**2)
def bmi_category(bmi):
    if bmi<18.5:
        return "Underweight"
    elif bmi<25:
        return "normal"
    elif bmi<30:
        return "overweight"
    elif bmi<35:
        return "obesity I"
    elif bmi<40:
        return "obesity II"
    else:
        return "obesity III"
df["BMI_class"]=df["BMI"].apply(bmi_category)
st.subheader("Heatmap hubungan pola makan (NCP) terhadap CAEC")
caec_order=["no", "Sometimes", "Frequently", "Always"]
heatmap_data=pd.crosstab(df["NCP_num"], df["CAEC"]).reindex(index=order_ncp, columns=caec_order)
fig_heatmap=px.imshow(
    heatmap_data,
    labels=dict(x="CAEC", y="Meals (NCP)", color="Jumlah orang"),
    x=caec_order,
    y=order_ncp,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="Blues"
)
fig_heatmap.update_layout(
    title="Heatmap Distribusi Populasi: Frekuensi Makan vs Kebiasaan Ngemil",
    xaxis_title="Konsumsi Makanan Selingan (CAEC)",
    yaxis_title="Jumlah Makan Utama per Hari (NCP)"
)
st.plotly_chart(fig_heatmap)