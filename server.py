import server_socket
from views import read_html

HOST = 'localhost'
PORT = 3235
# В зависимости от запроса клиента, будет выводиться соотвествующая информация
# http://localhost:3235/blog выведет информацию из шаблона blog.html
URL = {
    '/': 'templates/index.html',
    '/blog': 'templates/blog.html',
}


# Делим запрос с помощью команды сплит на массив слов и берем из него метод и url
def parsed_request(request):
    if not request:
        return 'GET', '/'
    method, url, *_ = request.split(' ')
    return method, url


# В зависимости от метода и url возвращаем заголок с кодом ответа
# \n\n отделяет наш заголовок от основного тела ответа
def generate_headers(method, url):
    if method != 'GET':
        return 'HTTP/1.1 405 Method not allowed\n\n', 405
    if url not in URL:
        return 'HTTP/1.1 404 Not found\n\n', 404

    return 'HTTP/1.1 200 OK\n\n', 200


# Генерируем наш ответ клиенту
# 1) Возьмем метод и адрес, который использовал клиент при отправке запроса
# 2) Сгенерируем заголовок, чтобы браузер смог прочитать наши данные и код ответа
# 3) Вернем заголовок и данные, которые содержит URL в словаре. После этого переводим
#    в понятный для сокетов тип(bytes) нашу строку
def generate_response(request):
    method, url = parsed_request(request)
    headers, code = generate_headers(method, url)
    html_doc = read_html(URL.get(url, '/')) if url in URL else 'Not data'
    return f'{headers} {html_doc}'.encode()


def run_server():
    # Создаем наш серверный сокет задав ему хост и порт(принцип работы и создание сокета смотреть
    # в модуле server_socket)

    s_socket = server_socket.init_socket(HOST, PORT)
    while True:
        # Методом accept выполнение блокируется, и ожидается входящее подключение.
        # При подключении клиента возвращается новый объект сокета,
        # который представляет собой подключение и кортеж с адресом клиента.
        cl_socket, addr = s_socket.accept()

        # После того как клиент сделает запрос, нам нужно забрать у него данные
        # Для этого выозовем метод recv, в котором нужно указать количество байт в пакете
        # После чего декодируем данные в utf-8, так как они присылаются нам в формате bytes
        request = cl_socket.recv(1024).decode('utf-8')

        # Можно посмотреть с какого адреса и порта завязывается подключение
        print(f'client address - {addr}\n')
        print(request)
        # Генерируем ответ клиенту
        response = generate_response(request)

        # Отправляем данные на клиентский сокет
        cl_socket.send(response)

        # Закрываем соединение, чтобы увидеть изменения в браузере
        cl_socket.close()


if __name__ == '__main__':
    run_server()
