#ARG ubuntu_version=18.04
#FROM ubuntu:${ubuntu_version}
#Use ubuntu 18:04 as your base image
FROM ubuntu:18.04
#Any label to recognise this image.
LABEL image=Spark-base-image
ENV SPARK_VERSION=2.4.4
ENV HADOOP_VERSION=2.7
#Run the following commands on my Linux machine
#install the below packages on the ubuntu image
RUN apt-get update -qq && \
    apt-get install -qq -y gnupg2 wget openjdk-8-jdk scala && \
    apt-get install -y git 
RUN apt-get install -y maven
#Download the Spark binaries from the repo
WORKDIR /
RUN wget --no-verbose http://mirrors.estointernet.in/apache/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz
# Untar the downloaded binaries , move them the folder name spark and add the spark bin on my class path
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