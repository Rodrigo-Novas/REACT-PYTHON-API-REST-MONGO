FROM python:3.9-alpine

WORKDIR /home

ENV FLASK_APP __main__.py
ENV FLASK_RUN_HOST 0.0.0.0

# RUN apk update && apk add --no-cache gcc libc-dev make git Libffi-dev openssl-dev python3-dev libxm12-dev libxslt-dev
RUN apk add --no-cache gcc musl-dev linux-headers

COPY . .

RUN pip install -r requirements.txt

CMD ["flask", "run"]