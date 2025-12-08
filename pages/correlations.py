import streamlit as st
import pandas as pd
from utils import ChiSquareTest, PearsonTest

df = pd.read_csv("./assets/dataset.csv")

params: dict[str, str] = {
    "MTRANS": "Transportation used",
    "CALC": "Consumption of alcohol",
    "CAEC": "Consumption of food between meals",
    "FCVC": "Frequency of consumption of vegetables"
}

st.subheader("Pearson test")
pt: PearsonTest = PearsonTest(
    df[["Age", "Height", "Weight", "FCVC", "NCP", "CH2O", "FAF", "TUE", "BMI"]]
)
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
