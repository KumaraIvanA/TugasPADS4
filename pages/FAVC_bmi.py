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
        df = pd.read_csv("assets/dataset.csv", sep=",")
    except:
        df = pd.read_csv("assets/dataset.csv", sep=";")
    return df


df = load_data()
st.subheader("proporsi tiap BMI per FAVC")
df["BMI"] = df["Weight"] / (df["Height"] ** 2)


def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "normal"
    elif bmi < 30:
        return "overweight"
    elif bmi < 35:
        return "obesity I"
    elif bmi < 40:
        return "obesity II"
    else:
        return "obesity III"


df["BMI_class"] = df["BMI"].apply(bmi_category)
temp = df.groupby(["FAVC", "BMI_class"]).size()
prop = (temp / temp.groupby(level=0).sum() * 100).to_frame("percentage")
proportion_df = prop.reset_index()

fig_proportion = px.bar(
    proportion_df,
    x="FAVC",
    y="percentage",
    color="BMI_class",
    title="persentase kategori BMI dalam tiap kelompok FAVC (frequently high calorie food)",
    barmode="group",
    text="percentage",
)
fig_proportion.update_traces(texttemplate="%{text:.2f}%", textposition="inside")
st.plotly_chart(fig_proportion)
st.subheader("hasil Chi-Square")
contingency = pd.crosstab(df["FAVC"], df["BMI_class"])
stats, p, dof, expected = chi2_contingency(contingency)
st.write("chi-square test: NCP vs BMI_class")
st.write("P-value", p)
st.write("Contingency table:")
st.dataframe(contingency)
