FROM python:3.7

RUN pip install fastapi uvicorn pandas

EXPOSE 80

COPY /get_matching_ids/src /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]