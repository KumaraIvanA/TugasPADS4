import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline #buat memodelkan regresi
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

#buat page di streamlit dengan judul dan layout berikut
st.set_page_config(page_title="Regresi Linear BMI", layout="wide")
#baca file csv
df = pd.read_csv("C:/Users/keisy/materi/sem 3/pads/Tugas 4/TugasPADS4/assets/normalizedDataset.csv")

#Sumbu X adalah kolom selain data frame di kolom ini (prediktor)
x = df.drop(columns = ["SMOKE", "Gender", "Weight", "Height", "NObeyesdad", "BMI", "cek", "BMI_Category"])
#BMI sebagai Sumbu y (target)
y = df["BMI"]

model_pipeline = Pipeline([
    ('scaler', MinMaxScaler()), #Menyamakan skala data (0-1)
    ('regress', LinearRegression())
])

#Latih Model
model_pipeline.fit(x, y)

# --- AMBIL KOEFISIEN ---
#Ambil model regresi dari dalam pipeline
# test size : ambil 20 persen data untuk tes model, random state : memerintah scikit untuk ambil data random untuk memastikn tes dan train datanya sama
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42) # test size : ambil 20 persen data untuk tes model, random state : memerintah scikit untuk ambil data random
model = model_pipeline.named_steps['regress']
model_pipeline.fit(x_train, y_train)
y_pred = model_pipeline.predict(x_test)

r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("R-Squared (Akurasi)", f"{r2:.2%}")
with col2:
    st.metric("Mean Absolute Error", f"{mae:.2f}")
with col3:
    st.metric("Mean Squared Error", f"{mse:.2f}")

#bobot setiap prediktor & intercept
intercept = model_pipeline.named_steps["regress"].intercept_
coefficients = model_pipeline.named_steps["regress"].coef_
st.metric("Intercept", intercept)
st.dataframe(
    pd.DataFrame(
        {
            "feature": x.columns,
            "coefficient": model_pipeline.named_steps["regress"].coef_,
        }
    )
)




