FROM alpine:3.18.3
LABEL Name=yorkorthodox=0.0.1

ARG USER_ID=1000
ARG GROUP_ID=1000

RUN apk update && \
    apk add --no-cache python3 py3-pip git sudo openssh sqlite py3-pytest

RUN addgroup -g ${GROUP_ID} -S user && \
    adduser -u ${USER_ID} -S user -G user -s /bin/sh && \
    echo "user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/sudoers

# Copy your Flask application code into the container
COPY . /app
RUN chown -R user:user /app
RUN pip3 install -r /app/requirements.txt

EXPOSE 5000
ENV PYTHONPATH /app/app

WORKDIR /app/calendar
RUN ./_build.sh

WORKDIR /app/scripts
RUN ./generate_service_db.py

USER user
WORKDIR /app

CMD ./run.sh
