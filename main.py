import firebase_admin
from firebase_admin import credentials, firestore
import tkinter as tk
import time
import threading
from datetime import datetime

# ===== CONFIGURAÇÃO DO FIREBASE =====
cred = credentials.Certificate("/home/Saboya/Downloads/bancodehoras-2ed45-firebase-adminsdk-fbsvc-5f6bc55a9f.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

start_time = None
running = False
usuario = "luna"

# ===== FUNÇÃO PARA SALVAR NO FIREBASE =====
def registrar_tempo(usuario, horas):
    data = datetime.now().strftime("%d-%m-%Y")
    doc_ref = db.collection("horas_trabalho").document(f"{usuario}_{data}")
    doc_ref.set({
        "usuario": usuario,
        "data": data,
        "horas_trabalhadas": horas
    })
    status_label.config(text="Tempo registrado no Firebase!")

# ===== FUNÇÕES DO TIMER =====
def update_timer():
    while running:
        elapsed = time.time() - start_time
        mins, secs = divmod(int(elapsed), 60)
        horas = mins // 60
        mins = mins % 60
        timer_label.config(text=f"{horas:02d}:{mins:02d}:{secs:02d}")
        time.sleep(1)

# ===== INICIAR E PARAR =====
def iniciar():
    global start_time, running
    if not running:
        start_time = time.time()
        running = True
        status_label.config(text="Trabalhando...")
        threading.Thread(target=update_timer, daemon=True).start()

def parar():
    global running
    if running:
        running = False
        tempo_total = time.time() - start_time
        horas_trabalhadas = round(tempo_total / 3600, 2)
        registrar_tempo(usuario, horas_trabalhadas)
        status_label.config(text=f"Trabalho finalizado: {horas_trabalhadas}h")

# ===== INTERFACE GRÁFICA =====
root = tk.Tk()
root.title("Controle de horas")
root.geometry("350x200")
root.resizable(False, False)

timer_label = tk.Label(root, text="00:00:00", font=("Helvetica", 40))
timer_label.pack(pady=10)

status_label = tk.Label(root, text="Clique em Iniciar", font=("Helvetica", 12))
status_label.pack(pady=5)

btn_iniciar = tk.Button(root, text="Iniciar", font=("Helvetica", 12), width=10, command=iniciar)
btn_iniciar.pack(side="left", padx=20, pady=20)

btn_parar = tk.Button(root, text="Parar", font=("Helvetica", 12), width=10, command=parar)
btn_parar.pack(side="right", padx=20, pady=20)

root.mainloop()
