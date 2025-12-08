import streamlit as st
import pandas as pd
from utils import ChiSquareTest, PearsonTest

df = pd.read_csv("./assets/normalizedDataset.csv")

params: dict[str, str] = {
    "FCVC": "Transportation used",
    "NCP": "Transportation used",
    "CAEC": "Consumption of food between meals",
    "CH2O": "Transportation used",
    "FAF": "Transportation used",
    "TUE": "Transportation used",
    "CALC": "Consumption of alcohol",
    "MTRANS": "Transportation used",
}

st.subheader("Pearson test")
pt: PearsonTest = PearsonTest(df[["Age", "BMI"]])
st.plotly_chart(pt.figure)


for param in params.keys():
    st.subheader(f"{param} ({params[param]})")
    cst = ChiSquareTest(df[param], df["NObeyesdad"])
    st.dataframe(cst.contingency_table)
    if cst.pvalue <= 0.05:
        st.badge(f"P Value: {cst.pvalue}", icon=":material/check:", color="green")
    else:
        st.badge(f"P Value: {cst.pvalue}", icon=":material/close:", color="red")
    st.text(f"Crammers V: {cst.crammers_v}")
    st.divider()
