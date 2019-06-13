FROM ubuntu

RUN apt-get update

RUN apt-get install -y python3.5


RUN apt-get install -y git

RUN mkdir /home/python

RUN cd /home/python

RUN git clone https://github.com/LucDamhuis/simulation.git

RUN apt-get install -y python3-pip --reinstall

RUN pip3 install openrouteservice

RUN pip3 install geopy

RUN pip3 install folium

RUN pip3 install pika

RUN apt-get install -y openssh-server

RUN mkdir /var/run/sshd

RUN echo 'root:password' | chpasswd

RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"

RUN echo "export VISIBLE=now" >> /etc/profile


EXPOSE 22

