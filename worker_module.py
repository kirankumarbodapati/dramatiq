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






MONGODB_URL="mongodb://mongodb:27017"
DATABASE_NAME="monodb_database"
COLLECTION_NAME="mogodb_collection"


client=AsyncIOMotorClient(MONGODB_URL)
database=client.get_database(DATABASE_NAME)
collection=database.get_collection(COLLECTION_NAME)













print(os.environ)
redis_host=os.environ["REDIS_URL"]
broker=RedisBroker(url="redis://redis_svc:6379")
dramatiq.set_broker(broker)
broker.add_middleware(AsyncIO())
broker.add_middleware(Middleware())

backend=RedisBackend(url="redis://redis_svc:6379")
broker.add_middleware(Results(backend=backend))
broker.declare_queue("default")








@dramatiq.actor(store_results=True)
def first_number(list1):
  a=random.choice(list1)
  return a



@dramatiq.actor(store_results=True)
def second_number(list1):
     b=random.choice(list1)
     return b



@dramatiq.actor(store_results=True)
async def multiplication(list2,task_id):
       print("hi")
       final_result=1
       for i in list2:
            final_result*=i
       await collection.insert_one({"task_id" : task_id,"task": "group" , "result": final_result})
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

    