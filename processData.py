import pandas as pd

df = pd.read_csv("./assets/dataset.csv")

df["Age"] = df["Age"].astype(int)
df["FCVC"] = df["FCVC"].astype(int)
df["NCP"] = df["NCP"].astype(int)
df["CH2O"] = df["CH2O"].astype(int)
df["FAF"] = df["FAF"].astype(int)
df["TUE"] = df["TUE"].astype(int)

# tambah kolom bmi
df["BMI"] = df["Weight"] / (df["Height"] ** 2)
bins = [0, 18.5, 25, 27.5, 30, 35, 40, 100]
labels = [0, 1, 2, 3, 4, 5, 6]
df["BMI"] = pd.cut(df["BMI"], bins=bins, labels=labels)

df.to_csv("./assets/cleanedDataset.csv", index=False)

# normalise gender dengan one hot encoding
# ubah nilai string ke 0 1
df["Gender"] = df["Gender"].replace({"Male": 1, "Female": 0})

# normalise family history dengan one hot encoding
# ubah nilai string ke 0 1
df["family_history_with_overweight"] = df["family_history_with_overweight"].replace(
    {"yes": 1, "no": 0}
)

# normalise pencatatan konsumsi makanan tinggi kalori
# ubah nilai 0 1 ke string
df["FAVC"] = df["FAVC"].replace({"yes": 1, "no": 0})

# normalise penctatan konsumsi makanan di luar jam makan dengan ordinal encoding
mapping = {"no": 0, "Sometimes": 1, "Frequently": 2, "Always": 3}
df["CAEC"] = df["CAEC"].map(mapping)

# normalise indikator merokok atau tidak dengan one hot encoding
df["SMOKE"] = df["SMOKE"].replace({"yes": 1, "no": 0})

# normalise monitoring konsumsi kalori harian
df["SCC"] = df["SCC"].replace({"yes": 1, "no": 0})

# normalise pencatatan konsumsi alkohol dengan ordinal encoding
mapping = {"no": 0, "Sometimes": 1, "Frequently": 2, "Always": 3}
df["CALC"] = df["CALC"].map(mapping)

# normalise transportasi yang digunakan
mapping = {
    "Automobile": 0,
    "Motorbike": 1,
    "Bike": 2,
    "Public_Transportation": 3,
    "Walking": 4,
}
df["MTRANS"] = df["MTRANS"].map(mapping)

# normalise kategori obesitas
mapping = {
    "Insufficient_Weight": 0,
    "Normal_Weight": 1,
    "Overweight_Level_I": 2,
    "Overweight_Level_II": 3,
    "Obesity_Type_I": 4,
    "Obesity_Type_II": 5,
    "Obesity_Type_III": 6,
}
df["NObeyesdad"] = df["NObeyesdad"].map(mapping)


df["cek"] = df["BMI"] == df["NObeyesdad"]

df.to_csv("./assets/normalizedDataset.csv", index=False)
