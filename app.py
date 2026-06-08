import webview
import subprocess
import threading
import time
import socket
import sys

def start_server():
    # inicia o Django usando o mesmo Python que está rodando o script
    subprocess.Popen([sys.executable, "manage.py", "runserver", "127.0.0.1:8000"])

def wait_for_server(host="127.0.0.1", port=8000):
    while True:
        s = socket.socket()
        try:
            s.connect((host, port))
            s.close()
            break
        except:
            time.sleep(1)

# iniciar servidor em paralelo
threading.Thread(target=start_server, daemon=True).start()

# esperar servidor ficar pronto
wait_for_server()

# abrir janela do app
webview.create_window("EstetiCar", "http://127.0.0.1:8000")

webview.start()
