# FROM centos:centos8
FROM python:3.9

ENV RMQ_HOST=15.237.25.152 \
    RMQ_PORT=5672 \
    RMQ_LOGIN=devops \
    RMQ_PASS=softserve \
    QUEUE_SLACK=slack \
    QUEUE_RESTAPI=restapi \
    HOST=0.0.0.0 \
    PORT=5000


# RUN dnf update -y \
#     dnf install python3 -y \
    # && pip3 install requests \
    # && pip3 install pika \
    # && pip3 install Flask \
    # && pip3 install python-dotenv

RUN apt-get update && apt-get install -y \
    && pip3 install requests \
    && pip3 install pika \
    && pip3 install Flask \
    && pip3 install python-dotenv


WORKDIR /root

COPY . .

EXPOSE 5000

ENTRYPOINT [ "python3", "jsonfilter.py" ]

# CMD ["python3", "/home/ec2-user/jsonFilter.py"]

# ENTRYPOINT [ "python3" ]

# CMD [ "/home/ec2-user/jsonFilter.py" ]


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