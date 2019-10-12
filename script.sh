#!/bin/bash

redis-server &
spark/bin/spark-submit --jars spark-redis/target/spark-redis-2.4.1-SNAPSHOT-jar-with-dependencies.jar spark.py Datafiniti_Womens_Shoes_Jun19.csv &
cd app/
python app.py
