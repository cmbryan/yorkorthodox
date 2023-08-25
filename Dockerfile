FROM alpine:3.18.3
LABEL Name=yorkorthodox=0.0.1

ARG USER_ID=1000
ARG GROUP_ID=1000

RUN addgroup -g ${GROUP_ID} -S user
RUN adduser -u ${USER_ID} -S user -G user -s /bin/sh

RUN apk update && \
    apk add --no-cache python3 py3-pip git curl

# Set the working directory
WORKDIR /app

# Copy your Flask application code into the container
COPY . /app
RUN pip3 install --user -r rest/requirements.txt -r site/requirements.txt

EXPOSE 8000
EXPOSE 5000

USER user

# Command to run the Flask application
CMD ["bash", "./run.sh"]
