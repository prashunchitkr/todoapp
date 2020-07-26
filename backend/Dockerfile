FROM python:alpine

COPY . /app

WORKDIR  /app

RUN apk add build-base postgresql-dev

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install psycopg2-binary

#RUN alembic upgrade head

EXPOSE 80

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "80"]
