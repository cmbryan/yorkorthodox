FROM alpine:3.18.3
LABEL Name=yorkorthodox=0.0.1

ARG USER_ID=1000
ARG GROUP_ID=1000

RUN addgroup -g ${GROUP_ID} -S user && \
    adduser -u ${USER_ID} -S user -G user -s /bin/bash && \
    mkdir -p /etc/sudoers.d && \
    echo "user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/sudoers

RUN apk update && \
    apk add --no-cache python3 py3-pip git sudo openssh sqlite py3-pytest bash

COPY .devcontainer/requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
