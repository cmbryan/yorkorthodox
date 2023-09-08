FROM alpine:3.18.3
LABEL Name=yorkorthodox=0.0.1

ARG USER_ID=1000
ARG GROUP_ID=1000

RUN addgroup -g ${GROUP_ID} -S user && \
    adduser -u ${USER_ID} -S user -G user -s /bin/sh
COPY sudoers /etc/sudoers.d/sudoers

RUN apk update && \
    apk add --no-cache python3 py3-pip git curl sudo openssh sqlite py3-pytest

# Set the working directory
WORKDIR /app

# Copy your Flask application code into the container
COPY . /app
RUN pip3 install -r requirements.txt -r rest/requirements.txt -r site/requirements.txt

EXPOSE 8000 5000

USER user
