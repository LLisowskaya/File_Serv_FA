import socket

# Устанавливаем соединение
HOST = 'localhost'
PORT = 9090
while True:
 # Подключаемся к серверу
 sock = socket.socket()
 sock.connect((HOST, PORT))
 # Получаем команду
 request = input('myftp@shell$ ')

 # Если это закачка
 if request.startswith("upload "):
   # Получаем исходное имя
   ref = request.split(" ")[1]
   # Получаем имя на сервере
   willbe = request.split(" ")[2]

   # Читаем данные
   myfile = open(ref, "r")
   data = myfile.read()
   myfile.close()
   
   # Получаем их длину
   datasize = len(data)
   # Отправляем на сервер имя файла, длину, и данные
   request = "upload " + willbe + " " + str(datasize) + " " + data

 # Если это скачка
 if request.startswith("download "):
   # То серверу не нужно знать, куда мы сохраним файл
   xref = request.split(" ")[1]
   xwillbe = request.split(" ")[2]
   # Передадим ему лишь имя желаемого файла
   request = "download " + xref

 # Отправляем запрос
 sock.send(request.encode())

 # Если запрос - exit, выходим из клиента
 if request == "exit":
   break;

 # Получаем ответ
 response = sock.recv(8192).decode()

 # Если ответа нет
 if not response:
    print("No data was received")
 else:
   # Если мы скачивали
   if request.startswith("download "):
        # Получаем размер ответа
        filesize = int(response.split(' ')[0])
        # Получаем содержимое файла
        sodfile = response[-filesize-1:]

        # Сохраняем его
        myfile = open(xwillbe, "w")
        myfile.write(sodfile)
        myfile.close()

        response = "File was downloaded"

   # Печатаем ответ
   print(response)

 # Закрываем сокет
 sock.close()
