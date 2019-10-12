from flask_restful import Resource
import logging as logger
import redis
from datetime import datetime

r = redis.StrictRedis(host='localhost', port=6379, db=0,
                      charset="utf-8", decode_responses=True)


class TaskByID(Resource):

    def post(self, taskId):
        logger.debug("Inside the post method of TaskById")
        return {"message": "Inside post method of TaskByID. TaskId : {}".format(taskId)}, 200

    def get(self, taskId):
        logger.debug(
            "Inisde the get method of TaskById. TaskID = {}".format(taskId))
        if taskId.startswith('getRecentItem'):
            s = r.hgetall(taskId)
            return s, 200
        elif taskId.startswith('getBrandsCount'):
            keys = r.keys(pattern=taskId+'*')
            val=[]
            for i in range(0,len(keys)) :
                a=r.hgetall(keys[i]);
                a['count']=int(a['count']);
                val.append(a)  
            newlist=sorted(val, key = lambda k:k['count'],reverse=True)
            return newlist,200
        elif taskId.startswith('getItemsByColor'):
            keys = r.keys(pattern=taskId+'*')
            val=[]
            for i in range(0,len(keys)):
                a=r.hgetall(keys[i])
                val.append(a)
            val.sort(key = lambda x: datetime.strptime(x['dateAdded'],"%Y-%m-%d"),reverse = True)
            return val[:10],200


    
    
    
    
    
   

    
