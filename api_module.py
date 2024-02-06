from worker_module import broker,collection
from worker_module import first_number,second_number,multiplication
from worker_module import addition1,addition2,addition3,addition4,addition5
from worker_module import subtraction1,subtraction2,subtraction3
from worker_module import backend
import time 
import dramatiq
from dramatiq.middleware import Middleware
from dramatiq.middleware import Pipelines
from dramatiq.middleware import AsyncIO
from dramatiq.results import Results , ResultBackend
from dramatiq.results.backends import RedisBackend
from dramatiq.results.errors import ResultTimeout
from dramatiq.brokers.redis import RedisBroker
import redis
import random
import os
from motor.motor_asyncio import AsyncIOMotorClient
from  fastapi import FastAPI, Depends
from datetime import datetime, timedelta

'''from http.server import BaseHTTPRequestHandler, HTTPServer

import prometheus_client as prom
import prometheus_client.multiprocess as prom_mp'''

#from dramatiq.middleware.from datetime import datetime, timedeltahealth_checks import DefaultHealthCheck




app=FastAPI()

messages={}

@app.post('/create_task/')
def create_task():
    task_id=len(messages)+1

    list1=[1,2,3,4,5,7,8,9,10]
    list2=[]

    g=dramatiq.group([
        first_number.message(list1),
        second_number.message(list1)
        
    ]).run()

    g.wait(timeout=10_000)

    for response in g.get_results(block=True):
             list2.append(response)
    print(list2)



    message=multiplication.send(list2,task_id)




    messages[task_id]=message
    print(messages)
    
    return {"task_id" : task_id}










@app.post('/create_pipeline/')
async def create_pipeline():
     task_id=len(messages)+1
     pipe= dramatiq.pipeline([
          
                 addition1.message(),
                 addition2.message(),
                 addition3.message()
                 
               
          ]).run()
     

     
     
     
     final_addition=pipe.get_result(block=True)
     
     await collection.insert_one({"task_id": task_id,"task":"pipeline","final_result":final_addition })

     return final_addition
   









@app.post('/create_new_links/')
async def create_new_links():
     
     task_id=len(messages)+1
     list2=[]
     list3=[]
     list4=[]
     g1=dramatiq.group([
          addition1.message(),
          addition2.message()
     ]).run()

     for response in g1.get_results(block=True):
          list2.append(response)
     print(list2)


     g2=dramatiq.group([
          addition2.message(),
          addition3.message()
     ]).run()
     for response in g2.get_results(block=True):
          list3.append(response)
     print(list3)





     g=dramatiq.group([
          addition4.message(list2),
          addition5.message(list3)
     ]).run()

     
     for response in g.get_results(block=True):
          list4.append(response)

     await collection.insert_one({"task_id": task_id,"operation": "multiple_groups","final_result": list4})
     return list4




     





@app.post('/create_group_of_pipelines/')
async def create_group_of_pipelines():
     task_id=len(messages)+1
     g=dramatiq.group([
          subtraction1.message()| 
          subtraction2.message()|
          subtraction3.message()
          
     ]).run()

     final_result=g.get_results(block=True)
     await collection.insert_one({"task_id": task_id,"operation": "group_of_pipelines","final_result":final_result})
     
     return final_result



         




     


@app.get('/get_task_status/{task_id}')
async def get_task_status(task_id : int):
   print(messages.keys())
   if task_id not in messages.keys(): 
       print("please enter a valid task_id")
       return
   
   
        
   
   try:
        result=messages[task_id].get_result(backend=backend, block=False)
        print(result)
        if result:
          document=await collection.find_one({"task_id": task_id})
          return  f"{document}"
         
        else:
            return {f"Task {task_id} is in progress"}
        
        

   except ResultTimeout as resultTimeout:
       return "resultTimeout"
       


   except dramatiq.results.ResultError as resulterror:
         return str(resulterror)

   except :
       return {f" Task {task_id} is in progress"}
   




@app.get('/health_check/')
async def health_check():
     return {"success" : "ok"}




'''def health():

      try:
          broker.ping()

          for worker in broker.workers:
               if not worker.is_alive():
                     return False
          return True
     
      except:
           return False
      

while True:
     health_status=health()
     print(health_status)
     time.sleep('''





'''def check_dramatiq_health(max_inactive_time=300):  
    try:
        
        broker.ping()

        for worker in broker.workers:
            last_activity_time = worker.last_activity_time

            if last_activity_time is not None:
           
                time_since_last_activity = datetime.utcnow() - last_activity_time

                if time_since_last_activity.total_seconds() > max_inactive_time:
                
                    return False
            else:
          
                return False

        return True

    except Exception as e:
        print(e)
        return False'''




'''from http.server import BaseHTTPRequestHandler, HTTPServer

import prometheus_client as prom
import prometheus_client.multiprocess as prom_mp'''


'''class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        registry = prom.CollectorRegistry()
        prom_mp.MultiProcessCollector(registry)
        output = prom.generate_latest(registry)
        self.send_response(200)
        self.send_header("content-type", prom.CONTENT_TYPE_LATEST)
        self.end_headers()
        self.wfile.write(output)


def server_forever():
    try:
        httpd = HTTPServer("0.0.0.0", MetricsHandler)
        httpd.serve_forever()
    except KeyboardInterrupt: 
        httpd.shutdown()

    return 0'''

      


        
   
