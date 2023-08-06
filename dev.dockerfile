FROM python:3.11
LABEL authors="jnbdz"

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
        telnet \
        iputils-ping \
        net-tools \
        vim \
        curl \
        wget \
        tree \
        cron \
        openssh-server

RUN pip3 install --upgrade pip && \
    pip3 install poetry

#RUN echo 'root:root' | chpasswd && \
#    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
#    sed -i 's/#Port 22/Port 22/' /etc/ssh/sshd_config

#RUN echo "alias ll='ls -l'" >> ~/.bashrc && \
#    echo "alias la='ls -la'" >> ~/.bashrc

#CMD service ssh start
