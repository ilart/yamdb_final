FROM python:3.7-slim
LABEL author='Arteev Ilia' version=1

WORKDIR /app
COPY requirements.txt ./
RUN pip3 install -r requirements.txt --no-cache-dir

COPY api api_yamdb reviews templates users manage.py ./

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind" , "0:8000"]

