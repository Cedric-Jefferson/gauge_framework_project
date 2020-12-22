FROM docker-hub.artifactory.molexcloud.com/python:3.7.9-alpine3.12
RUN apk update && apk add zip unzip wget curl iputils linux-headers bash alpine-sdk xvfb-run libressl-dev musl-dev libffi-dev py3-cryptography libxml2-dev libxslt-dev
RUN wget https://github.com/getgauge/gauge/releases/download/v1.0.7/gauge-1.0.7-linux.x86_64.zip && unzip -o gauge-1.0.7-linux.x86_64.zip -d /usr/local/bin
RUN pip3 install --upgrade pip
RUN pip3 install getgauge==0.3.9 grpcio==1.28.1 requests py3tftp gazpacho pyserial gazpacho pylogix selenium pyvirtualdisplay opcua cryptography ixnetwork_restpy python-periphery
RUN gauge install python -v 0.3.9
RUN gauge install flash -v 0.0.2
RUN gauge install html-report -v 4.0.9
RUN gauge install json-report -v 0.3.5
RUN gauge install screenshot -v 0.0.1

