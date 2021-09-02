FROM python:3.8-slim

COPY /requirements_docker.txt /home

RUN pip install -r /home/requirements_docker.txt 

COPY /src /home

WORKDIR /home
EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]