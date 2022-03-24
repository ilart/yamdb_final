FROM python:3.7-slim
LABEL author='Arteev Ilia' version=1

WORKDIR /app
COPY api_yamdb/ ./
RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind" , "0:8000"]

