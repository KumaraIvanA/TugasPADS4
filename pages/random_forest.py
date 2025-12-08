from sklearn.ensemble import RandomForestClassifier
import plotly.express as px
import streamlit as st
import pandas as pd
df_norm = pd.read_csv("assets/normalizedObesity.csv")
st.subheader("Faktor gaya hidup paling berpengaruh")
X=df_norm.drop(columns=["NObeyesdad", "Weight", "Height", "BMI"])
y=df_norm["NObeyesdad"]
model=RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X,y)
importance_df=pd.DataFrame({
    'Feature':X.columns,
    "Importance": model.feature_importances_
}).sort_values(by="Importance", ascending=True)
fig_imp=px.bar(
    importance_df,
    x='Importance',
    y='Feature',
    orientation='h',
    title="Ranking pengaruh gaya hidup terhadap Obesitas"
)
st.plotly_chart(fig_imp)
