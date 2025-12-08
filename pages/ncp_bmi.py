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
df["NCP"]=np.round(df["NCP"].astype(int))
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
contingency=pd.crosstab(df["NCP_num"], df["BMI_class"])
stats, p, dof, expected = chi2_contingency(contingency)
st.write("chi-square test: NCP vs BMI_class")
st.write("P-value", p)
st.write("Contingency table:")
st.dataframe(contingency)
st.write(df["NCP"].unique())
st.subheader("bar chart populasi tiap BMI & NCP")
count_df=df.groupby(["BMI_class", "NCP_num"]).size().reset_index(name="countBMI_NCP")
fig_bmi_ncp=px.bar(
    count_df,
    x="BMI_class",
    y="countBMI_NCP",
    color="NCP_num",
    barmode="group",
    labels={
        "BMI_class":"kategori BMI",
        "count": "jumlah orang",
        "NCP_num":"Jumlah makan per hari (NCP)"
    },
    title="Distribusi BMI berdasarkan kategori Jumlah makan per hari (NCP)"
)
fig_bmi_ncp.update_layout(
    xaxis_title="Kategori BMI",
    yaxis_title="Jumlah",
    legend_title="Kategori NCP",
    bargap=0.15,
    bargroupgap=0.1
)

st.plotly_chart(fig_bmi_ncp)
st.subheader("proporsi populasi BMI")
bmi_counts=df["BMI_class"].value_counts().reset_index()
bmi_counts.columns=["BMI_class", "count"]
fig_populationBmi=px.pie(
    bmi_counts, 
    names="BMI_class",
    values="count",
    title="Ditribusi populasi berdasarkan kategori BMI"
)
st.plotly_chart(fig_populationBmi)