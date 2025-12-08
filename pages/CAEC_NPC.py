import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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
st.subheader("heatmap pearson correlation NCP & CAEC")
caec_mapping_corr = {"no": 0, "Sometimes": 1, "Frequently": 2, "Always": 3}
df["CAEC_numeric"] = df["CAEC"].map(caec_mapping_corr)
df_Numeric=df[["NCP", "CAEC_numeric"]]
co_mtx=df_Numeric.corr(numeric_only=True)
print(co_mtx)
fig, ax=plt.subplots(figsize=(6,4))
sns.heatmap(
    co_mtx,
    cmap="YlGnBu",
    annot=True,
    fmt=".2f",
    vmin=-1, vmax=1,
    ax=ax
)
st.pyplot(fig)