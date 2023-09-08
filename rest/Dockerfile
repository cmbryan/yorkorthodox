FROM alpine:3.18.3
LABEL Name=yorkorthodox=0.0.1

ARG USER_ID=1000
ARG GROUP_ID=1000

RUN addgroup -g ${GROUP_ID} -S user && \
    adduser -u ${USER_ID} -S user -G user -s /bin/sh
COPY sudoers /etc/sudoers.d/sudoers

RUN apk update && \
    apk add --no-cache python3 py3-pip git curl sudo openssh sqlite py3-pytest

# Copy your Flask application code into the container
COPY . /app
WORKDIR /app
RUN chown -R user:user /app
RUN pip3 install -r requirements.txt

EXPOSE 5000
ENV PYTHONPATH /app

RUN ./build.sh

USER user

ENTRYPOINT gunicorn -b 0.0.0.0:5000 --reload app.yorkorthodox_rest:app
