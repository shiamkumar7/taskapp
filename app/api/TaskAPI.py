from flask_restful import Resource
import logging as logger
import redis

r=redis.StrictRedis(host = 'localhost',port =6379,db=0,charset="utf-8",decode_responses=True)


class Task(Resource):

    def post(self):
        logger.debug("Inside the post method of Task")
        return {"message" : "Inside post method"},200


    def get(self):
        logger.debug("Inisde the get method of Task")
        s=r.hgetall("occupation:IT")
        return s,200

    def put(self):
        logger.debug("Inisde the put method of Task")
        return {"message" : "Inside put method"},200

    def delete(sef):

        logger.debug("Inisde the delete method of Task")
        return {"message" : "Inside delete method"},200






