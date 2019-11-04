import os
import redis
import socket
import json

HOST=''
PORT=65432

prefix=os.environ['PREFIX']+":"

def put(key, value):
   cache = redis.Redis(host='rediska', port=6379)
   cache.ping()
   if cache.exists(key):
       cache.delete(key)
       mess = "Ok"
   else:
       mess = "Created"
   cache.set(key, json.dumps(value))
   if cache.exists(key):
      return json.dumps({"status": mess})
   else:
      return json.dumps({"status": "Internal Server Error"})

def sendMsg(conn, mess):
   conn.sendall(mess.encode('utf-8'))
   
def get(key):
   cache = redis.Redis(host='rediska', port=6379)
   cache.ping()
   if cache.exists(key):
      return json.dumps({"status": "Ok", "message": json.loads(cache.get(key))})
   else:
      return json.dumps({"status": "Not Found"})

def delete(key):
   cache = redis.Redis(host='rediska', port=6379)
   cache.ping()
   if cache.exists(key):
        cache.delete(key)
        return json.dumps({"status": "Ok"})
   else:
      return json.dumps({"status": "Not Found"})

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
               response = json.dumps({"status": "Bad Request"})
               sendMsg(conn, response)
               break
            else:
               request = json.loads(data.decode('utf-8'))
               response=""
               if request["action"] == "put":
                  response = put(request["key"], request["message"])
               elif request["action"] == "get":
                  response = get(request["key"])
               elif request["action"] == "delete":
                  response = delete(request["key"])
               else:
                  response = json.dumps({"status": "Bad Request"})
            sendMsg(conn, response)
