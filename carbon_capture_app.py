import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Veri hazırlama ve model eğitimi
np.random.seed(42)
num_samples = 1000
data = {
    "sicaklik": np.random.uniform(50, 200, num_samples),
    "basinc": np.random.uniform(1, 10, num_samples),
    "co2_konsantrasyonu": np.random.uniform(5, 20, num_samples),
    "gaz_akıs_hızı": np.random.uniform(0.5, 5.0, num_samples),
    "enerji_yogunlugu": np.random.uniform(100, 500, num_samples),
    "calisma_suresi": np.random.uniform(1, 24, num_samples),
    "cozucu_turu_amin": np.random.randint(0, 2, num_samples),
    "cozucu_turu_aktif_karbon": np.random.randint(0, 2, num_samples),
    "cozucu_turu_zeolit": np.random.randint(0, 2, num_samples),
    "cozucu_turu_MOF": np.random.randint(0, 2, num_samples),
    "reaktor_tasarimi_kolon": np.random.randint(0, 2, num_samples),
    "reaktor_tasarimi_membran": np.random.randint(0, 2, num_samples),
    "reaktor_tasarimi_adsorpsiyon": np.random.randint(0, 2, num_samples),
    "depolama_yontemi_kimyasal_donusum": np.random.randint(0, 2, num_samples),
    "depolama_yontemi_yer_alti_depolama": np.random.randint(0, 2, num_samples),
    "depolama_yontemi_sıvılaştırma": np.random.randint(0, 2, num_samples),
}

df = pd.DataFrame(data)

# Karbon yakalama oranı (örnek bir hedef değişken)
def calculate_capture_rate(row):
    capture_rate = 60
    capture_rate -= (row["sicaklik"] - 50) * 0.1
    capture_rate += (row["basinc"] - 1) * 2.5
    capture_rate += (row["co2_konsantrasyonu"] - 5) * 1.5
    capture_rate -= row["gaz_akıs_hızı"] * 4
    capture_rate += (row["enerji_yogunlugu"] - 100) * 0.05
    capture_rate -= (row["calisma_suresi"] - 8) * 0.5
    if row["cozucu_turu_amin"] == 1:
        capture_rate += 5
    elif row["cozucu_turu_aktif_karbon"] == 1:
        capture_rate += 2
    elif row["cozucu_turu_MOF"] == 1:
        capture_rate += 4
    elif row["cozucu_turu_zeolit"] == 1:
        capture_rate += 3
    if row["depolama_yontemi_kimyasal_donusum"] == 1:
        capture_rate += 2
    elif row["depolama_yontemi_yer_alti_depolama"] == 1:
        capture_rate += 1
    elif row["depolama_yontemi_sıvılaştırma"] == 1:
        capture_rate += 1.5
    return min(max(capture_rate, 0), 100)

df["karbon_yakalama_oranı"] = df.apply(calculate_capture_rate, axis=1)

# Modeli eğit
X = df.drop("karbon_yakalama_oranı", axis=1)
y = df["karbon_yakalama_oranı"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
feature_names = X.columns.tolist()

# Tkinter arayüzü
def predict_capture_rate():
    try:
        # Kullanıcı girişlerini al
        inputs = []
        for entry in entries:
            value = float(entry.get())
            inputs.append(value)

        # Girişleri tahmin için hazırlayın
        input_array = np.array([inputs])
        prediction = model.predict(input_array)
        
        # Tahmini göster
        messagebox.showinfo("Prediction", f"Predicted Carbon Capture Rate: {prediction[0]:.2f}%")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numerical values!")

# Tkinter uygulamasını oluştur
window = tk.Tk()
window.title("Carbon Capture Rate Predictor")

# Giriş alanları için bir liste
entries = []

# Özellik adlarına göre giriş kutuları oluştur
for i, feature in enumerate(feature_names):
    tk.Label(window, text=feature).grid(row=i, column=0, padx=10, pady=5)
    entry = tk.Entry(window)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries.append(entry)

# Tahmin butonu
predict_button = tk.Button(window, text="Predict", command=predict_capture_rate)
predict_button.grid(row=len(feature_names), column=0, columnspan=2, pady=10)

# Uygulamayı başlat
window.mainloop()
