import time 
import dramatiq
from dramatiq.middleware import Middleware
from dramatiq.middleware import pipelines
import fastapi
from dramatiq.results import Results , ResultBackend
from dramatiq.results.backends import RedisBackend
from dramatiq.results.errors import ResultTimeout
import random




app=fastapi.FastAPI()

messages={}










broker=dramatiq.get_broker()
broker.add_middleware(Middleware())
#broker.add_middleware(pipelines)
#broker.add_middleware(Results())
backend=RedisBackend()
broker.add_middleware(Results(backend=backend))
broker.declare_queue("default")
#broker.add_middleware(pipelines)




@dramatiq.actor(store_results=True)
def first_number(list1):
    a=random.choice(list1)
    return a



@dramatiq.actor(store_results=True)
def second_number(list1):
    b=random.choice(list1)
    return b



@dramatiq.actor(store_results=True)
def multiplication(list2):
      print("hi")
      final_result=1
      for i in list2:
           final_result*=i
      return final_result




@dramatiq.actor(store_results=True)
def addition1():
     x=2
     y=x+2
     return y

@dramatiq.actor(store_results=True)
def addition2():
     z=5
     a=z+2
     
     return a

@dramatiq.actor(store_results=True)
def addition3():
     z=5
     return z


@dramatiq.actor(store_results=True)
def addition4(list2):
     total=0
     for i in  list2:
          total+=i
     return total

          

@dramatiq.actor(store_results=True)
def addition5(list3):
    total=0
    for i in list3:
         total+=i
    return total
         

     
   


@app.post('/create_task/')
async def create_task():
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



    message=multiplication.send(list2)

        
   





    
    #first_number.send(list1)
    #second_number.send(list1)
    
    
    
    
    
    
    
   
    messages[task_id]=message
    print(messages)
    
    return {"task_id" : task_id}


@app.post('/create_pipeline/')
def create_pipeline():
     task_id=len(messages)+1
     #x=5
     #m=6
     pipe=dramatiq.pipeline([
          
                 addition1.message(),
                 addition2.message(),
                 addition3.message()
                 #addition3.message(pipe_ignore=True),
                 #addition4.message(),
                 #addition5.message(),
               
          ]).run()
     
     
          
          #addition1.message()|
          #addition2.message()|
          #addition3.message()
          #addition4.message(),
          #addition5.message()



     

     final_addition=pipe.get_result(block=True)
     return final_addition
     '''list3=[]
     for response in pipe.get_results(block=True):
          if response:
             list3.append(response)
          else:
               continue
     return list3'''


@app.post('/create_new_links/')
async def create_new_links():
     #list1=[1,23,4,5,6,7,8,9,10]
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
     return list4



@dramatiq.actor(store_results=True)
def subtraction1():
     x=20
     return x

@dramatiq.actor(store_results=True)
def subtraction2(x):
     y=x-2
     return y

@dramatiq.actor(store_results=True)
def subtraction3(y):
     z=y-2
     return z

     





@app.post('/create_group_of_pipelines/')
async def create_group_of_pipelines():
     g=dramatiq.group([
          subtraction1.message()| 
          subtraction2.message()|
          subtraction3.message()
          
     ]).run()

     final_result=g.get_results(block=True)
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
          return {"task_id":task_id , "status":"completed","result": result}
        else:
            return {f"Task {task_id} is in progress"}
        
        

   except ResultTimeout as resultTimeout:
       return "resultTimeout"
       


   except dramatiq.results.ResultError as resulterror:
         return str(resulterror)

   except :
       return {f" Task {task_id} is in progress"}
        
   
