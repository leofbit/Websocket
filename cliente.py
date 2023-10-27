import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 1234

CINZA = '#121212'
CINZA2 = '#1F1B24'
AZUL = '#464EB8'
BRANCO = "white"
FONTE = ("Helvetica", 17)
FONTE15 = ("Helvetica", 15)
FONTE13 = ("Helvetica", 13)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

def connect():
    try:
        client.connect((HOST, PORT))
        print("Conectado com o sucesso!")
        add_message("[SERVIDOR] Conectado com o sucesso!")
    except:
        messagebox.showerror("Falha na conexão", f"Falha na conexão {HOST} {PORT}")

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Nome inválido", "Nome não pode ser vazio")

    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

def send_message():
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0, len(message))
    else:
        messagebox.showerror("Nenhuma mensagem", "Mensagem não pode ser vazia")

root = tk.Tk()
root.geometry("600x600")
root.title("Cliente")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg=CINZA)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=CINZA2)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=CINZA)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_frame, text="Nome:", font=FONTE, bg=CINZA, fg=BRANCO)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONTE, bg=CINZA2, fg=BRANCO, width=23)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="Entrar", font=FONTE15, bg=AZUL, fg=BRANCO, command=connect)
username_button.pack(side=tk.LEFT, padx=15)

message_textbox = tk.Entry(bottom_frame, font=FONTE, bg=CINZA2, fg=BRANCO, width=38)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(bottom_frame, text="Enviar", font=FONTE15, bg=AZUL, fg=BRANCO, command=send_message)
message_button.pack(side=tk.LEFT, padx=10)

message_box = scrolledtext.ScrolledText(middle_frame, font=FONTE13, bg=CINZA2, fg=BRANCO, width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)


def listen_for_messages_from_server(client):

    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("~")[0]
            content = message.split('~')[1]
            add_message(f"[{username}] {content}")
        else:
            messagebox.showerror("Erro", "Mensagem enviada ao cliente esta vazia")

def main():

    root.mainloop()
    
if __name__ == '__main__':
    main()