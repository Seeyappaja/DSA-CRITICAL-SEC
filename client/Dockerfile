#
# Zookeeper client node demo container image
#

FROM ghcr.io/maxotta/kiv-ds-docker:latest

RUN yum -q -y install python3
RUN pip3 install kazoo

COPY python /opt/app
COPY script /opt/script
RUN chmod 777 /opt/script/script.sh
CMD /opt/script/script.sh 


# EOF
