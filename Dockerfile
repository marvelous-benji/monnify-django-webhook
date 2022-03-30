FROM python:3.9-slim

WORKDIR /app/

COPY db.sqlite3 manage.py requirements.txt README.md .
COPY webhook /app/webhook
COPY monnify /app/monnify

ARG MONNIFY_IP=35.242.133.146

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "manage.py", "runserver" ]

