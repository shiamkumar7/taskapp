
FROM ubuntu:18.04
LABEL image=Spark-base-image
ENV SPARK_VERSION=2.4.4
ENV HADOOP_VERSION=2.7

RUN apt-get update -qq && \
    apt-get install -qq -y gnupg2 wget openjdk-8-jdk scala && \
    apt-get install -y git 
RUN apt-get install -y maven

WORKDIR /
RUN wget --no-verbose http://mirrors.estointernet.in/apache/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz

RUN tar -xzf /spark-2.4.4-bin-hadoop2.7.tgz && \
    mv spark-2.4.4-bin-hadoop2.7 spark && \
    echo "export PATH=$PATH:/spark/bin" >> ~/.bashrc

RUN git clone https://github.com/RedisLabs/spark-redis.git 

RUN apt-get install -y redis && \
    apt-get install -y redis-server

RUN apt-get install -y python-pip && \
    apt-get install python

WORKDIR /spark-redis
RUN mvn clean package -DskipTests

ADD script.sh /
RUN chmod 777 /script.sh
#CMD /script.sh

WORKDIR /
ADD spark.py /
ADD Datafiniti_Womens_Shoes_Jun19.csv /

RUN pip install redis

ADD app /app
WORKDIR /app
RUN pip --no-cache-dir install -r requirements.txt

#Expose the UI Port 5000
EXPOSE 5000
WORKDIR /
CMD /script.sh
