

import tkinter as tk
from tkinter import messagebox
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

# Maliyet hesaplama fonksiyonu
def calculate_cost(row):
    cost = 0
    # Sıcaklık: Her 10 derece arttığında maliyet artar
    cost += (row["sicaklik"] - 50) * 0.2  
    # Basınç: Yüksek basınç daha fazla enerji tüketir
    cost += (row["basinc"] - 1) * 10  
    # CO2 Konsantrasyonu: Yüksek CO2 konsantrasyonu işleme maliyetini artırır
    cost += (row["co2_konsantrasyonu"] - 5) * 5  
    # Gaz Akışı Hızı: Yüksek hız, daha fazla enerji gerektirir
    cost += row["gaz_akıs_hızı"] * 2  
    # Diğer parametreler: Enerji yoğunluğu ve çalışma süresi de maliyetle ilişkili
    cost += (row["enerji_yogunlugu"] - 100) * 0.1
    cost += (row["calisma_suresi"] - 8) * 1.5
    
    # Çözücü türlerine göre maliyet eklemeleri
    if row["cozucu_turu_amin"] == 1:
        cost += 10
    elif row["cozucu_turu_aktif_karbon"] == 1:
        cost += 8
    elif row["cozucu_turu_MOF"] == 1:
        cost += 15
    elif row["cozucu_turu_zeolit"] == 1:
        cost += 12
        
    # Depolama yöntemine göre maliyet eklemeleri
    if row["depolama_yontemi_kimyasal_donusum"] == 1:
        cost += 7
    elif row["depolama_yontemi_yer_alti_depolama"] == 1:
        cost += 5
    elif row["depolama_yontemi_sıvılaştırma"] == 1:
        cost += 10
        
    return max(cost, 0)

df["maliyet"] = df.apply(calculate_cost, axis=1)

# Modeli eğit
X = df.drop(["karbon_yakalama_oranı", "maliyet"], axis=1)
y = df[["karbon_yakalama_oranı", "maliyet"]]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model_capture_rate = LinearRegression()
model_cost = LinearRegression()

model_capture_rate.fit(X_train, y_train["karbon_yakalama_oranı"])
model_cost.fit(X_train, y_train["maliyet"])

# Tkinter arayüzü
def predict():
    try:
        # Kullanıcı girişlerini al
        inputs = []
        for entry in entries:
            value = float(entry.get())
            inputs.append(value)

        # Girişleri tahmin için hazırlayın
        input_array = np.array([inputs])
        capture_rate_prediction = model_capture_rate.predict(input_array)[0]
        cost_prediction = model_cost.predict(input_array)[0]

        # Tahmin değerlerini etiketlerde göster
        capture_rate_label.config(text=f"Predicted Capture Rate: {capture_rate_prediction:.2f}%")
        cost_label.config(text=f"Predicted Cost: {cost_prediction:.2f} USD")

        # Grafiklerin güncellenmesi
        update_capture_rate_impact_chart()
        update_cost_impact_chart()

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numerical values!")

# Karbon yakalama oranını etkileyen parametrelerin grafiği
def update_capture_rate_impact_chart():
    # Modelin katsayıları, her bir parametrenin etkisini gösterir
    coefficients = model_capture_rate.coef_
    fig.clear()
    ax = fig.add_subplot(121)
    ax.bar(X.columns, coefficients, color='blue')
    ax.set_ylabel("Impact on Capture Rate")
    ax.set_xticklabels(X.columns, rotation=45, ha="right")  # Etiketleri döndür
    ax.set_title("Capture Rate Impact by Feature")
    canvas.draw()

# Maliyet üzerine etkisi olan parametrelerin grafiği
def update_cost_impact_chart():
    # Modelin katsayıları, her bir parametrenin etkisini gösterir
    coefficients = model_cost.coef_
    fig.clear()
    ax = fig.add_subplot(122)
    ax.bar(X.columns, coefficients, color='red')
    ax.set_ylabel("Impact on Cost")
    ax.set_xticklabels(X.columns, rotation=45, ha="right")  # Etiketleri döndür
    ax.set_title("Cost Impact by Feature")
    canvas.draw()

# Tkinter uygulamasını oluştur
window = tk.Tk()
window.title("Carbon Capture Rate and Cost Predictor")

# İki sütun düzenlemesi
entries = []
for i, feature in enumerate(X.columns):
    col = i % 2  # 0 veya 1
    row = i // 2
    tk.Label(window, text=feature).grid(row=row, column=col * 2, padx=5, pady=5, sticky="e")
    entry = tk.Entry(window)
    entry.grid(row=row, column=col * 2 + 1, padx=5, pady=5)
    entries.append(entry)

# Predict butonu
predict_button = tk.Button(window, text="Predict", command=predict)
predict_button.grid(row=(len(X.columns) + 1) // 2, column=0, columnspan=4, pady=10)

# Karbon yakalama oranını ve maliyeti gösteren etiketler
capture_rate_label = tk.Label(window, text="Predicted Capture Rate: N/A", font=("Arial", 14), fg="blue")
capture_rate_label.grid(row=((len(X.columns) + 1) // 2) + 1, column=0, columnspan=4, pady=10)

cost_label = tk.Label(window, text="Predicted Cost: N/A", font=("Arial", 14), fg="red")
cost_label.grid(row=((len(X.columns) + 1) // 2) + 2, column=0, columnspan=4, pady=10)




# Uygulamayı başlat
window.mainloop()
