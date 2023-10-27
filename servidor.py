import socket
import threading

HOST = '127.0.0.1'
PORT = 1234 
LISTENER_LIMIT = 5
active_clients = [] 

def listen_for_messages(client, username):

    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            final_msg = username + '~' + message
            send_messages_to_all(final_msg)

        else:
            print(f"A mensagem enviada do cliente {username} está vazia")

def send_message_to_client(client, message):

    client.sendall(message.encode())

def send_messages_to_all(message):
    
    for user in active_clients:

        send_message_to_client(user[1], message)

def client_handler(client):
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = "SERVIDOR~" + f"{username} entrou no chat!"
            send_messages_to_all(prompt_message)
            break
        else:
            print("Nome cliente está vazio!")

    threading.Thread(target=listen_for_messages, args=(client, username, )).start()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
        print(f"Funcionando no host: {HOST} na porta: {PORT}")
    except:
        print(f"Erro no host: {HOST} na porta: {PORT}")

    server.listen(LISTENER_LIMIT)

    while 1:
        client, address = server.accept()
        print(f"Sucesso ao conectar {address[0]} {address[1]}")

        threading.Thread(target=client_handler, args=(client, )).start()


if __name__ == '__main__':
    main()