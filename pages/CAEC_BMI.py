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
st.subheader("proporsi tiap BMI per CAEC")
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
# df["TUE"]=np.floor(df["TUE"].astype(int))
count_df = df.groupby(["CAEC", "BMI_class"]).size()
prop = (count_df / count_df.groupby(level=0).sum() * 100).to_frame("percentage")
proportion_df = prop.reset_index()
fig_snack_BMI = px.bar(
    proportion_df,
    x="CAEC",
    y="percentage",
    color="BMI_class",
    barmode="group",
    title="frekuensi makan diantara meals (CAEC) per kategori BMI",
    text="percentage",
)

fig_snack_BMI.update_traces(texttemplate="%{text:.2f}%", textposition="inside")
st.plotly_chart(fig_snack_BMI)
contingency = pd.crosstab(df["CAEC"], df["BMI_class"])
stats, p, dof, expected = chi2_contingency(contingency)
st.write("chi-square test: CAEC vs BMI_class")
st.write("P-value", p)
st.write("Contingency table:")
st.dataframe(contingency)
