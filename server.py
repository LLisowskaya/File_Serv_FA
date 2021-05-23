import socket
import os
import glob

# Функция обработки запроса
def process(req):
 # Команда pwd, вернуть текущий каталог
 if req == 'pwd':
    return os.getcwd()
 # Команда ls
 elif req == 'ls':
    # Собрать в списке все файлы и каталоги
    files = []
    for filename in glob.iglob('**', recursive=True):
         files = files + [filename]
    # И вернуть список
    return '; '.join(files)
 else:
    # Если команда с параметрами, получаем их число
    reqs = req.split(" ")
    # Если параметров не два (команда + 1 параметр)
    if len(reqs) != 2:
        # Если меньше двух (только команда), ошибка
        if len(reqs) < 2:
            return 'bad request'
        # Если команда rename, переименовываем
        elif reqs[0] == 'rename':
          os.rename(reqs[1].replace('..', ''), reqs[2].replace('..', ''))
          return 'file was renamed if it can be done'
        # Если команда upload
        elif reqs[0] == 'upload':
          # Получаем имя и размер файла
          filename = reqs[1].replace('..', '')
          filesize = int(reqs[2])
          # Получаем данные файла
          sodfile = req[-filesize-1:]

          # Сохраняем данные в файл на сервере
          myfile = open(filename, "w")
          myfile.write(sodfile)
          myfile.close()
          return 'file was transferred'
        # Если три и более параметров, но не upload и не rename
        else:
             return 'bad request'
    # Если команда mkdir, создаем каталог
    elif reqs[0] == 'mkdir':
        os.mkdir(reqs[1].replace('..', ''))
        return 'directory created if not existed'
    # Если команда rmdir, удаляем каталог
    elif reqs[0] == 'rmdir':
        os.rmdir(reqs[1].replace('..', ''))
        return 'directory deleted, if existed'
    # Если команда rmfile, удаляем файл
    elif reqs[0] == 'rmfile':
        os.remove(reqs[1].replace('..', ''))
        return 'file deleted, if existed'
    # Если команда download, читаем требуемый файл
    elif reqs[0] == 'download':
        ref = req.split(" ")[1].replace('..', '')
        myfile = open(ref, "r")
        data = myfile.read()
        myfile.close()
 
        # И отдаем клиенту его длину и сами данные
        datasize = len(data)
        request = str(datasize) + " " + data
        return request
    # В противном случае - ошибка, неизвестная команда
    else:
        return 'bad request'

# Номер порта
PORT = 9090
# Переходим в нужный каталог
os.chdir("DATA")

# Вечный цикл
while True:
 # Создаем сокет
 print("Создаем новый сокет")
 sock = socket.socket()
 sock.bind(('' , PORT))
 sock.listen()

 # Вечный цикл
 while True:
  # Ждем подключений
  print('Слушаем порт', PORT)
  # Если кто-то подключился, выводим это
  conn, addr = sock.accept()
  print(addr)
  # Получаем команду
  request = conn.recv(8192).decode()
  print(request)
 
  # Если это выход, выходим и мы
  if request == "exit":
     break;
 
  # Обработать запрос
  response = process(request) + "\n"
  # Отправить ответ обратно
  conn.send(response.encode())

 # Если команда выход, закрыть сокет
 sock.close()
