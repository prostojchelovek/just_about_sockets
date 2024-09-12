import server_socket
from variables import HOST, PORT

# Этот скрипт был написан для наглядного примера последовательного выполнения кода
# в котором блокируется подключение нового клиента пока первый кто зашел не
# прервет подключение и даст возможность подключиться новому "клиенту"
server_socket = server_socket.init_socket(HOST, PORT)

while True:
    print('Before .accept()')
    client_socket, addr = server_socket.accept()
    print('Connection from:', addr)

    while True:
        print('Before .recv()')
        request = client_socket.recv(4096)
        print(request.decode('utf-8'))
        if not request:
            break
        else:
            response = 'Data client\n'.encode()
            client_socket.send(response)

    client_socket.close()
