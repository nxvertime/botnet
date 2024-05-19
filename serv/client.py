import socket 


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
s.connect(("127.0.0.1", 4444))
while True:
    i = input(">")
    s.send(i.encode('utf8'))
    res = s.recv(255).decode('utf8')
    print(res)