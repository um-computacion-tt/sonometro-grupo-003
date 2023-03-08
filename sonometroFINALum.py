import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Configuración de la grabación
FRAGMENTO= 1024 # Tamaño del búfer de audio
FORMATO = pyaudio.paInt16 # Formato de audio
CANALES = 1 # Número de canales de audio
TASA = 44100 # Tasa de muestreo (en Hz)
UMBRAL = 5000 # Umbral para la detección de sonido (ajusta este valor según sea necesario)

# Inicializador PyAudio
p = pyaudio.PyAudio()
stream= p.open(format=FORMATO,
                channels=CANALES,
                rate=TASA,
                input=True,
                frames_per_buffer=FRAGMENTO)

def obtener_dato_audio():
    data = stream.read(FRAGMENTO)
    data= np.frombuffer(data, dtype=np.int16)
    return data 
    

def mostrar_espectro(i):
    data = obtener_dato_audio()
    hfft_data = np.abs(np.fft.hfft(data))[:len(data)//2]
    freqs = np.fft.fftfreq(len(data), 1/44100)[:len(data)//2]
       
    # Configuracion de Espectro
    ax1.clear()
    ax1.plot (freqs,hfft_data)
    ax1.set_xlim (0,FRAGMENTO)
    ax1.set_ylim (-40000, 40000)

    # Configuracion del medidor de decibeles 
    db = 20*np.log10(np.sqrt(np.mean(data**2)))
    ax2.clear()
    ax2.text(0.5, 0.5, f'{db:.2f} dB', fontsize=48, ha='center', va='center')
    if db > 60:
        ax2.text(0.5, 0.2, 'Atencion nivel no seguro!', fontsize=48, ha='center', va='center', color='red')
    else:
        ax2.text(0.5, 0.2, 'Nivel Seguro', fontsize=48, ha='center', va='center', color='green')
fig, (ax1, ax2) = plt.subplots(nrows=2)  
# Propiedades del eje 
ax1.set_xlabel('Frequencia (Hz)')
ax1.set_ylabel('Amplitud')
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.axis('off')
#mostrar primer grafico 
def animacion(_):
    mostrar_espectro(_)

ani = FuncAnimation(fig, animacion, interval=50)
from matplotlib.widgets import Button

# Definicion de Botones
def inicio(event):
    stream.start_stream()
    ani.event_source.start()

def pausa(event):
    stream.stop_stream()
    ani.event_source.stop()

# Configuracion de Botones 
inicio_ax1 = plt.axes([0.7, 0.006, 0.1, 0.075])
inicio_button = Button(inicio_ax1, 'Inicio')
inicio_button.on_clicked(inicio)
pausa_ax1=plt.axes([0.81, 0.006, 0.1, 0.075])
pausa_button = Button(pausa_ax1, 'Pausa')
pausa_button.on_clicked(pausa)

# Mostrar graficos 
plt.show()

