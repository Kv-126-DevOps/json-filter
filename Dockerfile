# ===centos image===
#FROM centos:centos7

#RUN yum -y update

#RUN yum install python38 -y

#RUN pip3 install pika \
#    flask \
#    python-dotenv

#WORKDIR /root

#COPY . .

#EXPOSE 5000

#ENTRYPOINT [ "python3", "jsonfilter.py" ]



# ===ubuntu image===
 FROM python:3.9

 ENV RMQ_HOST=15.237.25.152 \
     RMQ_PORT=5672 \
     RMQ_LOGIN=devops \
     RMQ_PASS=softserve \
     QUEUE_SLACK=slack \
     QUEUE_RESTAPI=restapi \
     HOST=0.0.0.0 \
     PORT=5000
    
 RUN apt-get update && apt-get install -y \
     && pip3 install requests \
     && pip3 install pika \
     && pip3 install Flask \
     && pip3 install python-dotenv


 WORKDIR /root

 COPY . .

 EXPOSE 5000

 ENTRYPOINT [ "python3", "jsonfilter.py" ]


# ==how to install docker on centos==
# dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
# dnf install docker-ce
# systemctl start docker
# systemctl enable docker
# systemctl status docker
# firewall-cmd --zone=public --add-masquerade --permanent
# firewall-cmd --reload
# docker --version
# docker run hello-world
# dnf remove docker-ce
