from sklearn.ensemble import RandomForestClassifier
import plotly.express as px
import streamlit as st
import pandas as pd
df_norm = pd.read_csv("assets/dataset.csv")
st.subheader("Faktor gaya hidup paling berpengaruh")
df_norm['Gender'] = df_norm['Gender'].replace({"Male": 1, "Female": 0})
df_norm['family_history_with_overweight'] = df_norm['family_history_with_overweight'].replace({"yes":1, "no":0})
df_norm['FAVC'] = df_norm['FAVC'].replace({"yes":1, "no":0})
mapping = {"no":0, "Sometimes":1, "Frequently":2, "Always":3}
df_norm['CAEC'] = df_norm['CAEC'].map(mapping)

#normalise indikator merokok atau tidak dengan one hot encoding
df_norm['SMOKE'] = df_norm['SMOKE'].replace({"yes":1, "no":0})

#normalise monitoring konsumsi kalori harian
df_norm['SCC'] = df_norm['SCC'].replace({"yes":1, "no":0})

#normalise pencatatan konsumsi alkohol dengan ordinal encoding
mapping = {"no":0, "Sometimes":1, "Frequently":2, "Always":3}
df_norm['CALC'] = df_norm['CALC'].map(mapping)

#normalise transportasi yang digunakan
mapping = {"Automobile":0, "Motorbike":1, "Bike":2, "Public_Transportation":3, "Walking":4}
df_norm['MTRANS'] = df_norm['MTRANS'].map(mapping)

#normalise kategori obesitas
mapping = {"Insufficient_Weight":0, "Normal_Weight":1, "Overweight_Level_I":2, "Overweight_Level_II":3, "Obesity_Type_I":4, "Obesity_Type_II":5, "Obesity_Type_III":6}
df_norm['NObeyesdad'] = df_norm["NObeyesdad"].map(mapping)

X=df_norm.drop(columns=["NObeyesdad", "Weight", "Height"])
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
