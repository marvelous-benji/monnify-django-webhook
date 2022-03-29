FROM python:3.9-slim

WORKDIR /app/

COPY ../monify-django-webhook .

ARG MONNIFY_IP=35.242.133.146

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "manage.py", "runserver" ]

