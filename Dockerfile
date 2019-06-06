FROM lmnetworks/python3:3.6.8_20190523

# when possible install dependencies from Alpine packages
RUN apk add --no-cache py3-prettytable=0.7.2-r1 \
                       py3-dateutil=2.7.3-r0 py3-tz=2018.9-r0 py3-requests=2.19.1-r0 && \
    pip3 install influxdb==5.2.2

COPY . /src
WORKDIR /src
# --editable avoids a second useless copy
RUN pip3 install --editable .

ENTRYPOINT [ "dockerhub_stats" ]