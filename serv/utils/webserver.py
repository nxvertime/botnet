import aiohttp.web
import requests
import pathlib
import mysql.connector
import json
from utils.general import pmsg, sendCmd
##### WEB SERVER ######################################
async def api_dashboard(request):
    try:
        conn = mysql.connector.connect(user='root', password='',
                                    host='127.0.0.1',
                                    database='db_botnet')
    except mysql.connector.errors:
        print("[X] ERROR: Can't connect to db! exiting....")
        exit()
    
    curs = conn.cursor()
    curs.execute("SELECT * FROM tasks WHERE task_status = 1")
    
    rows = curs.fetchall()
    taskNbr = len(rows)
    
    curs.execute('''SELECT id
                    FROM victims
                    WHERE first_connection >= NOW() - INTERVAL 1 DAY;''')
    
    rows = curs.fetchall()
    lastVics = len(rows) 

    curs = conn.cursor()
    curs.execute('''SELECT latency_ms FROM victims WHERE status LIKE "connected";''')
    rows = curs.fetchall()
    sumLatency = 0
    #print(rows[0][0])
    for x in rows[0]:
        sumLatency += x
    avgLatency = round(sumLatency / len(rows[0]))
    avgLatency = f"{avgLatency}ms"

    curs = conn.cursor()
    curs.execute("SELECT id FROM interface_servers WHERE status = 1")
    
    rows = curs.fetchall()
    intServ = len(rows)

    data = {
        "taskNbr" : taskNbr,
        "lastVics" : lastVics,
        "avgLatency" : avgLatency,
        "intServ": intServ
    }


    jsonData = json.dumps(data, separators=(',', ':'))

    conn.close()
    return aiohttp.web.Response(status=200, body=jsonData, content_type="text/json")




async def handle_request(request):
    # Récupère le chemin de la requête
    rel_path = request.match_info['path']
    # Le chemin du répertoire webserver
    webserver_path = pathlib.Path(__file__).parent / '../webserver'
    # Le chemin absolu de la ressource demandée
    resource_path = webserver_path / rel_path
    # print(f"Webserv path: {webserver_path}")
    # print(f"resource path: {resource_path}")
    # Sécurité de base pour éviter le traversal de répertoires
    if '..' in rel_path or resource_path.is_dir() or not resource_path.exists():
        return aiohttp.web.Response(status=404, text='404: File not found')

    content_type = 'text/html'  # Par défaut, suppose que c'est du HTML
    if resource_path.suffix in ['.css']:
        content_type = 'text/css'
    elif resource_path.suffix in ['.js']:
        content_type = 'application/javascript'
    elif resource_path.suffix in ['.jpg', '.jpeg', '.png', '.gif']:
        content_type = 'image/' + resource_path.suffix.replace('.', '')

    content = resource_path.read_bytes()
    return aiohttp.web.Response(body=content, content_type=content_type)

async def web_server():
    app = aiohttp.web.Application()
    
    app.router.add_get('/api/getDashboard', api_dashboard)
    app.router.add_get('/{path:.*}', handle_request)
    
    
    # Run the web server on localhost and port 8080
    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    site = aiohttp.web.TCPSite(runner, 'localhost', 8080)
    await site.start()
    await pmsg("[v] Web server started on http://localhost:8080")

###############################################################
