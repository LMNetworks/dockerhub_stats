FROM lmnetworks/python3:3.7.4_20191014

# when possible install dependencies from Alpine packages
RUN apk add --no-cache py3-prettytable=0.7.2-r2 \
                       py3-dateutil=2.7.3-r1 py3-tz=2019.1-r0 py3-requests=2.21.0-r4 && \
    pip3 install influxdb==5.2.3

COPY . /src
WORKDIR /src
# --editable avoids a second useless copy
RUN pip3 install --editable .

ENTRYPOINT [ "dockerhub_stats" ]