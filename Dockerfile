FROM python:3.8-slim

COPY /id_graph_api/requirements_docker.txt /home

RUN pip install -r /home/requirements_docker.txt 

EXPOSE 80

COPY /id_graph_api/src /home

CMD ["uvicorn", "home.main:app", "--host", "0.0.0.0", "--port", "80"]