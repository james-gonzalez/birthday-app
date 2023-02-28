FROM alpine:3.17.2

RUN apk add --no-cache python3 py3-pip curl bash git

WORKDIR /opt

ADD app.py .
ADD requirements.txt .

RUN pip install -r /opt/requirements.txt

# EXPOSE 5000

ARG WERKZEUG_DEBUG_PIN=off

ENTRYPOINT [ "/usr/bin/python", "app.py" ]
