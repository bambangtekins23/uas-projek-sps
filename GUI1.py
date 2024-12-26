import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

def generate_signal(sensor_index):
    t = np.linspace(0, 24, 1000)  # waktu dalam jam
    if sensor_index == 0:  # Intensitas Cahaya
        return 10 + 10 * np.sin(2 * np.pi * t / 24) + np.random.normal(0, 0.5, len(t))
    elif sensor_index == 1:  # Radiasi Matahari
        return 15 + 8 * np.sin(2 * np.pi * t / 24) + np.random.normal(0, 0.5, len(t))
    elif sensor_index == 2:  # Kelembapan Udara
        return 70 + 5 * np.sin(2 * np.pi * t / 24) + np.random.normal(0, 0.5, len(t))
    elif sensor_index == 3:  # Temperatur Udara
        return 25 + 5 * np.sin(2 * np.pi * t / 24) + np.random.normal(0, 0.5, len(t))
    elif sensor_index == 4:  # Kecepatan Angin
        return 5 + 2 * np.sin(2 * np.pi * t / 24) + np.random.normal(0, 0.5, len(t))
    else:
        return np.zeros_like(t)

def apply_operation(signal, operation, freq):
    t = np.linspace(0, 24, len(signal))
    mod_signal = np.sin(2 * np.pi * freq * t / 24)
    if operation == "Tambah":
        return signal + mod_signal
    elif operation == "Kurang":
        return signal - mod_signal
    elif operation == "Kali":
        return signal * mod_signal
    elif operation == "Bagi":
        return signal / (mod_signal + 0.1)  # Hindari pembagian nol
    else:
        return signal

def plot_signals():
    sensor_index = sensor_var.get()
    operation = operation_var.get()
    freq = freq_var.get()

    original_signal = generate_signal(sensor_index)
    processed_signal = apply_operation(original_signal, operation, freq)

    # Plot sinyal asli
    ax1.clear()
    ax1.plot(t, original_signal, label="Sinyal Asli", color="blue")
    ax1.set_title("Sinyal Asli")
    ax1.set_xlabel("Waktu (jam)")
    ax1.set_ylabel("Amplitudo")
    ax1.legend()

    # Plot sinyal setelah operasi
    ax2.clear()
    ax2.plot(t, processed_signal, label=f"Sinyal Setelah Operasi ({operation})", color="green")
    ax2.set_title(f"Sinyal Setelah Operasi: {operation} dengan {freq:.1f} Hz")
    ax2.set_xlabel("Waktu (jam)")
    ax2.set_ylabel("Amplitudo")
    ax2.legend()

    # Plot DFT
    ax3.clear()
    fft_signal = np.abs(np.fft.fft(original_signal))
    freq_axis = np.fft.fftfreq(len(original_signal), d=(t[1] - t[0]))
    ax3.plot(freq_axis[:len(freq_axis)//2], fft_signal[:len(fft_signal)//2], color="purple", label="Spektrum Frekuensi")
    ax3.set_title("Transformasi Fourier Diskrit (DFT)")
    ax3.set_xlabel("Frekuensi (Hz)")
    ax3.set_ylabel("Magnitudo")
    ax3.legend()

    canvas.draw()

# GUI Utama
root = tk.Tk()
root.title("GUI Sinyal Sensor")
root.geometry("1200x800")
root.configure(bg="#FAF3DD")

# Data waktu
t = np.linspace(0, 24, 1000)

# Frame untuk plotting
plot_frame = tk.Frame(root, bg="#FAF3DD")
plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6, 8))
fig.tight_layout(pad=4)
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Frame untuk kontrol
control_frame = tk.Frame(root, bg="#C7EAE4", width=300)
control_frame.pack(side=tk.RIGHT, fill=tk.Y)

# Pilihan sensor
sensor_var = tk.IntVar(value=0)
tk.Label(control_frame, text="Pilih Sensor:", bg="#C7EAE4", font=("Arial", 12)).pack(anchor="w", pady=(10, 0))
sensors = ["Intensitas Cahaya", "Radiasi Matahari", "Kelembapan Udara", "Temperatur Udara", "Kecepatan Angin"]
for i, sensor in enumerate(sensors):
    tk.Radiobutton(control_frame, text=sensor, variable=sensor_var, value=i, bg="#C7EAE4", font=("Arial", 10)).pack(anchor="w")

# Pilihan operasi
operation_var = tk.StringVar(value="Tambah")
tk.Label(control_frame, text="Pilih Operasi:", bg="#C7EAE4", font=("Arial", 12)).pack(anchor="w", pady=(10, 0))
operations = ["Tambah", "Kurang", "Kali", "Bagi"]
for operation in operations:
    tk.Radiobutton(control_frame, text=operation, variable=operation_var, value=operation, bg="#C7EAE4", font=("Arial", 10)).pack(anchor="w")

# Slider frekuensi
freq_var = tk.DoubleVar(value=10)
tk.Label(control_frame, text="Frekuensi:", bg="#C7EAE4", font=("Arial", 12)).pack(anchor="w", pady=(10, 0))
freq_slider = ttk.Scale(control_frame, from_=0, to=50, variable=freq_var, orient="horizontal")
freq_slider.pack(fill="x", padx=20)

# Tombol untuk menampilkan sinyal
tk.Button(control_frame, text="Tampilkan Sinyal", command=plot_signals, bg="#1E88E5", fg="white", font=("Arial", 12)).pack(pady=10)

# Kotak identitas
identity_frame = tk.Frame(control_frame, bg="#FAF3DD", padx=10, pady=10, relief="ridge", borderwidth=2)
identity_frame.pack(fill="x", pady=(20, 0))
tk.Label(identity_frame, text="Nama: Bambang Pamart", bg="#FAF3DD", font=("Arial", 10)).pack(anchor="w")
tk.Label(identity_frame, text="NRP: 2024231016", bg="#FAF3DD", font=("Arial", 10)).pack(anchor="w")
tk.Label(identity_frame, text="Kelas: 3B", bg="#FAF3DD", font=("Arial", 10)).pack(anchor="w")

root.mainloop()
