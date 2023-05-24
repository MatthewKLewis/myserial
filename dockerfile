# IOx app needs base-rootfs. Select either 32 or 64 bit version by uncommenting out one of the below link.
# Use below link for 64 bit Access Points
# FROM devhub-docker.cisco.com/iox-docker/ir1101/base-rootfs:latest

# use below link for 32 bit Access Points, when cisco devhub is active.
# FROM devhub-docker.cisco.com/iox-docker/ap3k/base-rootfs:latest
# COPY main /usr/bin/main
# RUN chmod 777 /usr/bin/main

# meantime solution?
# pull base docker image for binary builds
FROM --platform=$TARGETARCH alpine:latest AS builder
RUN apk update
RUN apk upgrade
RUN apk add --no-cache build-base curl wget openssl rabbitmq-c jq

# download source for lrzsz binaries
RUN wget https://ohse.de/uwe/releases/lrzsz-0.12.20.tar.gz

#extract the source
RUN tar xvf lrzsz-0.12.20.tar.gz

# compile and install lrzsz binaries in /usr/local/bin/
RUN cd lrzsz-0.12.20 && ./configure
RUN cd lrzsz-0.12.20 && make
RUN cd lrzsz-0.12.20 && make install

# start from base rootfs again for the final docker image
FROM --platform=$TARGETARCH alpine:latest
RUN apk update
RUN apk upgrade
RUN apk add --no-cache curl wget openssl rabbitmq-c jq

# copy lrzsz compiled above in builder work space
COPY --from=builder /usr/local/bin/* /usr/bin/
COPY --from=builder /usr/local/lib/* /usr/lib/

COPY main /usr/bin/main
COPY package_config.ini /usr/bin/package_config.ini

RUN chmod 777 /usr/bin/main
RUN chmod 777 /usr/bin/package_config.ini